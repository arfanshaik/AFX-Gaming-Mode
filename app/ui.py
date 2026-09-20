import threading
import time
import tkinter.filedialog as fd
import tkinter.messagebox as mb

import customtkinter as ctk

from app.launcher import launch_game, wait_for_exit
from app.monitor import system_snapshot, heavy_background_processes
from app.profiles import PROFILES, get_profile, recommend_profile
from app.settings import load_settings, save_settings
from app.windows_tools import set_power_plan, open_game_mode_settings, open_task_manager

class GamingModeApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("AFX Gaming Mode")
        self.root.geometry("1040x700")
        self.root.minsize(900, 620)

        self.settings = load_settings()
        self.game_path = ctk.StringVar(value=self.settings.get("game_path", ""))
        self.profile = ctk.StringVar(value=self.settings.get("profile", "Balanced"))
        self.use_power = ctk.BooleanVar(value=self.settings.get("use_high_performance_power", True))
        self.auto_restore = ctk.BooleanVar(value=self.settings.get("auto_restore_power", True))

        self.game_process = None
        self.session_started = None
        self.monitor_running = True

        self._build()
        self._refresh_system()
        self._monitor_loop()

    def _build(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(self.root, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="AFX GAMING MODE",
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            header,
            text="Safe game launch • process priority • live PC monitoring • automatic restore",
            text_color="gray70"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

        setup = ctk.CTkFrame(self.root)
        setup.grid(row=1, column=0, sticky="ew", padx=18, pady=14)
        setup.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(setup, text="Game executable").grid(row=0, column=0, padx=12, pady=12, sticky="w")
        ctk.CTkEntry(setup, textvariable=self.game_path).grid(row=0, column=1, padx=8, pady=12, sticky="ew")
        ctk.CTkButton(setup, text="Browse", width=90, command=self._browse).grid(row=0, column=2, padx=12, pady=12)

        ctk.CTkLabel(setup, text="Profile").grid(row=1, column=0, padx=12, pady=10, sticky="w")
        ctk.CTkOptionMenu(
            setup,
            variable=self.profile,
            values=list(PROFILES.keys()),
            command=lambda _v: self._update_profile_text()
        ).grid(row=1, column=1, padx=8, pady=10, sticky="w")

        self.profile_text = ctk.CTkLabel(setup, text="", text_color="gray70")
        self.profile_text.grid(row=2, column=1, columnspan=2, padx=8, pady=(0, 10), sticky="w")
        self._update_profile_text()

        self.power_switch = ctk.CTkSwitch(
            setup,
            text="Use High Performance power plan",
            variable=self.use_power
        )
        self.power_switch.grid(row=3, column=1, padx=8, pady=8, sticky="w")

        self.restore_switch = ctk.CTkSwitch(
            setup,
            text="Restore Balanced power after game closes",
            variable=self.auto_restore
        )
        self.restore_switch.grid(row=4, column=1, padx=8, pady=(0, 14), sticky="w")

        cards = ctk.CTkFrame(self.root, fg_color="transparent")
        cards.grid(row=2, column=0, sticky="ew", padx=18)
        for i in range(4):
            cards.grid_columnconfigure(i, weight=1)

        self.cpu_card = self._metric_card(cards, 0, "CPU", "--")
        self.ram_card = self._metric_card(cards, 1, "RAM", "--")
        self.session_card = self._metric_card(cards, 2, "SESSION", "Idle")
        self.profile_card = self._metric_card(cards, 3, "PROFILE", self.profile.get())

        body = ctk.CTkFrame(self.root)
        body.grid(row=3, column=0, sticky="nsew", padx=18, pady=14)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(2, weight=1)

        action_row = ctk.CTkFrame(body, fg_color="transparent")
        action_row.grid(row=0, column=0, sticky="ew", padx=12, pady=12)

        self.launch_button = ctk.CTkButton(
            action_row,
            text="START GAMING MODE",
            height=44,
            command=self._launch
        )
        self.launch_button.pack(side="left")

        ctk.CTkButton(
            action_row,
            text="Game Mode Settings",
            command=self._game_mode_settings
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            action_row,
            text="Task Manager",
            command=self._task_manager
        ).pack(side="left")

        ctk.CTkLabel(
            body,
            text="Heavy background processes (view only)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=0, sticky="nw", padx=14, pady=(4, 0))

        self.process_box = ctk.CTkTextbox(body, height=170)
        self.process_box.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)
        self.process_box.configure(state="disabled")

        self.status = ctk.CTkLabel(self.root, text="Ready.", anchor="w")
        self.status.grid(row=4, column=0, sticky="ew", padx=22, pady=(0, 14))

    def _metric_card(self, parent, column, title, value):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=column, sticky="ew", padx=5)
        ctk.CTkLabel(frame, text=title, text_color="gray70").pack(pady=(12, 2))
        label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=(0, 12))
        return label

    def _browse(self):
        path = fd.askopenfilename(
            title="Choose game executable",
            filetypes=[("Windows executable", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.game_path.set(path)

    def _update_profile_text(self):
        profile = get_profile(self.profile.get())
        self.profile_text.configure(text=profile["description"])
        if hasattr(self, "profile_card"):
            self.profile_card.configure(text=self.profile.get())

    def _save(self):
        save_settings({
            "game_path": self.game_path.get().strip(),
            "profile": self.profile.get(),
            "use_high_performance_power": self.use_power.get(),
            "auto_restore_power": self.auto_restore.get(),
        })

    def _launch(self):
        if self.game_process and self.game_process.poll() is None:
            mb.showinfo("AFX Gaming Mode", "A game session is already active.")
            return

        path = self.game_path.get().strip()
        if not path:
            mb.showwarning("AFX Gaming Mode", "Choose a game executable first.")
            return

        self._save()
        profile = get_profile(self.profile.get())

        use_power = self.use_power.get() or profile.get("power_plan", False)
        process, message = launch_game(path, profile, use_high_performance_power=use_power)
        self.status.configure(text=message)

        if process is None:
            mb.showerror("Launch failed", message)
            return

        self.game_process = process
        self.session_started = time.time()
        self.launch_button.configure(text="GAME SESSION ACTIVE", state="disabled")

        thread = threading.Thread(target=self._watch_game, daemon=True)
        thread.start()

    def _watch_game(self):
        wait_for_exit(self.game_process)

        if self.auto_restore.get():
            set_power_plan(False)

        self.game_process = None
        self.session_started = None
        self.root.after(0, self._session_finished)

    def _session_finished(self):
        self.launch_button.configure(text="START GAMING MODE", state="normal")
        self.status.configure(text="Game session ended. Windows power mode restored when enabled.")
        self.session_card.configure(text="Idle")

    def _refresh_system(self):
        info = system_snapshot()
        self.cpu_card.configure(text=f"{info['cpu_percent']:.0f}%")
        self.ram_card.configure(text=f"{info['memory_percent']:.0f}%")

        suggested = recommend_profile(info)
        if not self.profile.get():
            self.profile.set(suggested)

        if self.session_started:
            elapsed = int(time.time() - self.session_started)
            minutes, seconds = divmod(elapsed, 60)
            self.session_card.configure(text=f"{minutes:02d}:{seconds:02d}")

        exclude = [self.game_process.pid] if self.game_process and self.game_process.poll() is None else []
        rows = heavy_background_processes(exclude_pids=exclude, limit=8)
        text = "\n".join(
            f"{row['name']:<28}  RAM {row['memory_percent']:>5.1f}%   CPU {row['cpu_percent']:>5.1f}%   PID {row['pid']}"
            for row in rows
        ) or "No process data available."

        self.process_box.configure(state="normal")
        self.process_box.delete("1.0", "end")
        self.process_box.insert("1.0", text)
        self.process_box.configure(state="disabled")

    def _monitor_loop(self):
        if not self.monitor_running:
            return
        self._refresh_system()
        self.root.after(2000, self._monitor_loop)

    def _game_mode_settings(self):
        ok, msg = open_game_mode_settings()
        self.status.configure(text=msg)
        if not ok:
            mb.showwarning("Game Mode", msg)

    def _task_manager(self):
        ok, msg = open_task_manager()
        self.status.configure(text=msg)
        if not ok:
            mb.showwarning("Task Manager", msg)

    def run(self):
        self.root.mainloop()
