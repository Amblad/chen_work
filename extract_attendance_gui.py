import threading
import traceback
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from extract_attendance import run_extraction


class AttendanceExtractorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("考勤表数据提取")
        self.root.geometry("640x420")
        self.root.minsize(560, 360)

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar(value="output.xlsx")
        self.status_var = tk.StringVar(value="请选择输入文件或文件夹")

        self._build_ui()

    def _build_ui(self) -> None:
        padding = {"padx": 12, "pady": 6}

        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        ttk.Label(main, text="考勤表数据提取", font=("Microsoft YaHei UI", 14, "bold")).pack(
            anchor=tk.W, pady=(0, 12)
        )

        input_frame = ttk.LabelFrame(main, text="输入", padding=10)
        input_frame.pack(fill=tk.X, **padding)

        ttk.Entry(input_frame, textvariable=self.input_var).pack(
            fill=tk.X, side=tk.TOP, pady=(0, 8)
        )

        input_btns = ttk.Frame(input_frame)
        input_btns.pack(fill=tk.X)
        ttk.Button(input_btns, text="选择文件", command=self._pick_file).pack(side=tk.LEFT)
        ttk.Button(input_btns, text="选择文件夹", command=self._pick_folder).pack(
            side=tk.LEFT, padx=(8, 0)
        )

        output_frame = ttk.LabelFrame(main, text="输出", padding=10)
        output_frame.pack(fill=tk.X, **padding)

        ttk.Entry(output_frame, textvariable=self.output_var).pack(
            fill=tk.X, side=tk.TOP, pady=(0, 8)
        )
        ttk.Button(output_frame, text="选择保存位置", command=self._pick_output).pack(
            anchor=tk.W
        )

        action_frame = ttk.Frame(main)
        action_frame.pack(fill=tk.X, **padding)
        self.run_btn = ttk.Button(action_frame, text="开始提取", command=self._start)
        self.run_btn.pack(side=tk.LEFT)

        log_frame = ttk.LabelFrame(main, text="日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, **padding)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=10, state=tk.DISABLED, wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, textvariable=self.status_var).pack(anchor=tk.W, pady=(4, 0))

    def _pick_file(self) -> None:
        path = filedialog.askopenfilename(
            title="选择 Excel 文件",
            filetypes=[("Excel 文件", "*.xlsx *.xlsm"), ("所有文件", "*.*")],
        )
        if path:
            self.input_var.set(path)

    def _pick_folder(self) -> None:
        path = filedialog.askdirectory(title="选择文件夹")
        if path:
            self.input_var.set(path)

    def _pick_output(self) -> None:
        path = filedialog.asksaveasfilename(
            title="保存输出文件",
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
        )
        if path:
            self.output_var.set(path)

    def _append_log(self, message: str) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _set_running(self, running: bool) -> None:
        state = tk.DISABLED if running else tk.NORMAL
        self.run_btn.configure(state=state)

    def _start(self) -> None:
        input_path = self.input_var.get().strip()
        output_path = self.output_var.get().strip()

        if not input_path:
            messagebox.showwarning("提示", "请先选择输入文件或文件夹")
            return
        if not output_path:
            messagebox.showwarning("提示", "请先设置输出文件路径")
            return

        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.status_var.set("正在处理...")
        self._set_running(True)

        thread = threading.Thread(
            target=self._run_task,
            args=(Path(input_path), Path(output_path)),
            daemon=True,
        )
        thread.start()

    def _run_task(self, input_path: Path, output_path: Path) -> None:
        try:
            total = run_extraction(input_path, output_path, log=self._log_threadsafe)
            self.root.after(0, self._on_success, total, str(output_path))
        except Exception:
            err_msg = traceback.format_exc()
            self.root.after(0, self._on_error, err_msg)

    def _log_threadsafe(self, message: str) -> None:
        self.root.after(0, self._append_log, message)

    def _on_success(self, total: int, output_path: str) -> None:
        self._set_running(False)
        self.status_var.set(f"完成，共提取 {total} 行")
        if total == 0:
            messagebox.showwarning(
                "完成",
                f"处理结束，但未提取到任何数据行。\n\n"
                f"请确认:\n"
                f"1. A 列是否为日期格式\n"
                f"2. 文件是否为 .xlsx / .xlsm 格式\n"
                f"3. 是否选择了正确的文件",
            )
        else:
            messagebox.showinfo("完成", f"已保存到:\n{output_path}\n\n共 {total} 行")

    def _on_error(self, message: str) -> None:
        self._set_running(False)
        self.status_var.set("处理失败")
        self._append_log(message)
        short_msg = message.strip().splitlines()[-1] if message else "未知错误"
        messagebox.showerror("错误", short_msg)


def main() -> None:
    root = tk.Tk()
    AttendanceExtractorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
