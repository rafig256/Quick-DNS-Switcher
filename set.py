import tkinter as tk
import subprocess
import sys
import os
import ctypes

# تابع برای چک کردن دسترسی Admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# تابع برای درخواست دسترسی Admin
def request_admin_rights():
    if not is_admin():
        # اگر دسترسی Admin نداریم، دوباره برنامه را با دسترسی Admin اجرا کن
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# تابع برای فعال کردن DNS خودکار
def enable_auto_dns(interface_index):
    try:
        result = subprocess.run(
            ["powershell", f"Set-DnsClientServerAddress -InterfaceIndex {interface_index} -ResetServerAddresses"],
            check=True,
            capture_output=True,
            text=True
        )
        status_label.config(text="DNS خودکار فعال شد.", fg="green")
    except Exception as e:
        status_label.config(text=f"خطا: {e}", fg="red")

# تابع برای تنظیم DNS سفارشی
def set_custom_dns(interface_index):
    dns1 = "178.22.122.100"
    dns2 = "185.51.200.2"
    try:
        result = subprocess.run(
            ["powershell", f"Set-DnsClientServerAddress -InterfaceIndex {interface_index} -ServerAddresses @('{dns1}','{dns2}')"],
            check=True,
            capture_output=True,
            text=True
        )
        status_label.config(text="DNS سفارشی تنظیم شد.", fg="green")
    except Exception as e:
        status_label.config(text=f"خطا: {e}", fg="red")

# تابع برای یافتن InterfaceIndex ادپاتر فعال
def get_active_interface_index():
    try:
        result = subprocess.run(
            ["powershell", "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object -First 1 -ExpandProperty InterfaceIndex"],
            check=True,
            capture_output=True,
            text=True
        )
        return int(result.stdout.strip())
    except Exception as e:
        status_label.config(text=f"خطا: نمی‌توان ادپاتر فعال را پیدا کرد. {e}", fg="red")
        return None

# درخواست دسترسی Admin
request_admin_rights()

# یافتن InterfaceIndex ادپاتر فعال
interface_index = get_active_interface_index()
if interface_index is None:
    sys.exit()  # خروج از برنامه اگر ادپاتر فعال پیدا نشد

# ایجاد پنجره GUI
root = tk.Tk()
root.title("تنظیم DNS")
root.geometry("350x150")

# لیبل وضعیت
status_label = tk.Label(root, text="وضعیت: منتظر عملیات...", fg="black")
status_label.pack(pady=10)

# دکمه خاموش (فعال کردن DNS خودکار)
off_button = tk.Button(
    root,
    text="خاموش (DNS خودکار)",
    command=lambda: enable_auto_dns(interface_index),
    bg="red",
    fg="white"
)
off_button.pack(pady=5, fill="x")

# دکمه روشن (تنظیم DNS سفارشی)
on_button = tk.Button(
    root,
    text="روشن (DNS سفارشی)",
    command=lambda: set_custom_dns(interface_index),
    bg="green",
    fg="white"
)
on_button.pack(pady=5, fill="x")

# اجرا کردن حلقه اصلی Tkinter
root.mainloop()
