import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
from threading import Thread

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickDown - YouTube Video Downloader")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL Entry input field 
        ttk.Label(self.main_frame, text="Enter YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Quality Selection
        ttk.Label(self.main_frame, text="Select Quality:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="1080p")
        self.quality_combo = ttk.Combobox(self.main_frame, textvariable=self.quality_var, 
                                        values=["2160p", "1440p", "1080p", "720p", "480p", "360p"], 
                                        state="readonly", width=20)
        self.quality_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Download Location
        ttk.Label(self.main_frame, text="Download Location:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.location_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.location_entry = ttk.Entry(self.main_frame, textvariable=self.location_var, width=40)
        self.location_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        self.browse_btn = ttk.Button(self.main_frame, text="Browse", command=self.browse_location)
        self.browse_btn.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, length=400, mode='determinate', 
                                          variable=self.progress_var)
        self.progress_bar.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready to download")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Download Button
        self.download_btn = ttk.Button(self.main_frame, text="Download", command=self.start_download_thread)
        self.download_btn.grid(row=7, column=0, columnspan=2, pady=10)
    
    def browse_location(self):
        directory = filedialog.askdirectory(initialdir=self.location_var.get())
        if directory:
            self.location_var.set(directory)
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total_bytes = d.get('total_bytes', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes:
                    percentage = (downloaded_bytes / total_bytes) * 100
                    self.progress_var.set(percentage)
                    self.status_var.set(f"Downloading... {percentage:.1f}%")
                    self.root.update()
            except Exception:
                pass
        elif d['status'] == 'finished':
            self.status_var.set("Download completed!")
            self.progress_var.set(100)
            
    def start_download_thread(self):
        Thread(target=self.start_download, daemon=True).start()
    
    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        try:
            self.download_btn.configure(state='disabled')
            self.status_var.set("Fetching video information...")
            self.root.update()
            
            quality = self.quality_var.get().replace('p', '')
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
                'outtmpl': os.path.join(self.location_var.get(), '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Success", "Video downloaded successfully!")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.progress_var.set(0)
            self.download_btn.configure(state='normal')
            self.status_var.set("Ready to download")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()