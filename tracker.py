import customtkinter as ctk
import requests
from datetime import datetime
import webbrowser
from packaging import version
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
import io
import threading

OWNER = "sleepsweetly"
REPO = "3D-Effect-Generator-for-MythicMobs-OBJ-PNG-"
GITHUB_API = f"https://api.github.com/repos/{OWNER}/{REPO}/releases"
GITHUB_REPO_URL = f"https://github.com/{OWNER}/{REPO}"
THEME_COLORS = {
    "dark_bg": "#0d1117",
    "darker_bg": "#010409",
    "header_bg": "#161b22",
    "accent": "#1f6feb",
    "text": "#c9d1d9",
    "text_secondary": "#8b949e",
    "success": "#238636",
    "danger": "#da3633",
    "warning": "#d29922"
}

class GitHubReleaseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("discord/yaslicadi ")
        self.geometry("1200x900")
        self.minsize(1000, 700)
        self.configure_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.data_loaded = False
        self.dark_mode = True
        self.fetch_data()

    def configure_ui(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=THEME_COLORS["dark_bg"])

        self.main_container = ctk.CTkFrame(self, corner_radius=12, fg_color=THEME_COLORS["darker_bg"])
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.header = ctk.CTkFrame(self.main_container, corner_radius=8, fg_color=THEME_COLORS["header_bg"], height=80)
        self.header.pack(fill="x", padx=10, pady=10)

        self.title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.title_frame.pack(side="left", padx=15, pady=10, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="GitHub Release Tracker",
            font=("Segoe UI", 24, "bold"),
            text_color=THEME_COLORS["text"]
        )
        self.title_label.pack(anchor="w")

        self.repo_label = ctk.CTkLabel(
            self.title_frame,
            text=f"{OWNER}/{REPO}",
            font=("Segoe UI", 14),
            text_color=THEME_COLORS["text_secondary"],
            cursor="hand2"
        )
        self.repo_label.pack(anchor="w")
        self.repo_label.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_REPO_URL))

        self.control_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.control_frame.pack(side="right", padx=15, pady=10)

        self.refresh_btn = ctk.CTkButton(
            self.control_frame,
            text="🔄 Refresh",
            font=("Segoe UI", 14, "bold"),
            width=120,
            height=40,
            corner_radius=8,
            text_color="white",
            fg_color=THEME_COLORS["accent"],
            hover_color="#2a7fff",
            command=self.fetch_data
        )
        self.refresh_btn.pack(side="left", padx=5)




        self.status_bar = ctk.CTkFrame(self.main_container, corner_radius=8, height=30, fg_color=THEME_COLORS["header_bg"])
        self.status_bar.pack(fill="x", padx=10, pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=("Segoe UI", 11),
            text_color=THEME_COLORS["text_secondary"]
        )
        self.status_label.pack(side="left", padx=15)

        self.stats_label = ctk.CTkLabel(
            self.status_bar,
            text="Total downloads: 0 | Last update: Never",
            font=("Segoe UI", 11),
            text_color=THEME_COLORS["text_secondary"]
        )
        self.stats_label.pack(side="right", padx=15)

        self.content_frame = ctk.CTkFrame(self.main_container, corner_radius=8, fg_color=THEME_COLORS["header_bg"])
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tabview = ctk.CTkTabview(self.content_frame, fg_color=THEME_COLORS["header_bg"])
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tab1 = self.tabview.add("Release Details")
        self.tab2 = self.tabview.add("Statistics")
        self.tab3 = self.tabview.add("About")
        self.release_text = ctk.CTkTextbox(
            self.tab1,
            wrap="none",
            font=("Consolas", 12),
            fg_color=THEME_COLORS["darker_bg"],
            text_color=THEME_COLORS["text"],
            corner_radius=8
        )
        self.release_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.release_text.insert("0.0", "Loading release data...\n\nPlease wait or click refresh button.")
        self.release_text.configure(state="disabled")


        self.stats_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        self.stats_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.stats_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


        about_text = f"""
        GitHub Release Tracker v1.0
        
        A comprehensive tool to track and analyze GitHub release statistics.
        
        Tracking: {OWNER}/{REPO}
        
        Features:
        - Detailed release information
        - Download statistics
        - Visual analytics
        
        Created with yaslicadi (sleepsweetly) using Python and CustomTkinter
        """
        self.about_text = ctk.CTkTextbox(
            self.tab3,
            wrap="word",
            font=("Segoe UI", 14),
            fg_color="transparent",
            text_color=THEME_COLORS["text"],
            height=200
        )
        self.about_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.about_text.insert("0.0", about_text)
        self.about_text.configure(state="disabled")

    def setup_icons(self):
        try:
            refresh_icon = self.load_icon("🔃", 20)
            theme_icon = self.load_icon("🌓", 20)
            
            self.refresh_btn.configure(image=refresh_icon, compound="left")
            self.theme_btn.configure(image=theme_icon, compound="left")
        except Exception as e:
            print(f"Error loading icons: {e}")

    def load_icon(self, emoji, size):
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        return ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))

    def fetch_data(self):
        self.refresh_btn.configure(state="disabled")
        self.status_label.configure(text="Fetching data from GitHub...")
        self.update_idletasks()
        
        threading.Thread(target=self._fetch_data_thread, daemon=True).start()

    def _fetch_data_thread(self):
        try:
            response = requests.get(GITHUB_API)
            if response.status_code != 200:
                self.show_error(f"API Error: {response.status_code}")
                return

            releases = response.json()
            if not releases:
                self.show_error("No releases found")
                return
            processed_data = []
            total_downloads = 0
            
            for release in releases:
                version_str = release["tag_name"]
                pub_date = datetime.strptime(release["published_at"], "%Y-%m-%dT%H:%M:%SZ")
                assets = release.get("assets", [])
                
                release_downloads = sum(asset["download_count"] for asset in assets)
                total_downloads += release_downloads
                
                processed_data.append({
                    "version": version_str,
                    "date": pub_date,
                    "assets": assets,
                    "total_downloads": release_downloads
                })

            try:
                processed_data.sort(key=lambda x: version.parse(x["version"]), reverse=True)
            except:
                processed_data.sort(key=lambda x: x["date"], reverse=True)

            self.after(0, self.update_ui, processed_data, total_downloads)
            
        except requests.exceptions.RequestException as e:
            self.after(0, self.show_error, f"Connection Error: {str(e)}")
        except Exception as e:
            self.after(0, self.show_error, f"Unexpected Error: {str(e)}")
        finally:
            self.after(0, lambda: self.refresh_btn.configure(state="normal"))

    def update_ui(self, releases, total_downloads):
        self.release_text.configure(state="normal")
        self.release_text.delete("0.0", "end")
        
        for release in releases:
            version_str = release["version"]
            date_str = release["date"].strftime("%Y-%m-%d")
            self.release_text.insert("end", f"╔═══════════════════════════════════════\n")
            self.release_text.insert("end", f"║ 🏷️ Release: {version_str}\n", "version")
            self.release_text.insert("end", f"║ 📅 Date: {date_str}\n", "date")
            self.release_text.insert("end", f"║ 📦 Total Downloads: {release['total_downloads']}\n", "total")
            self.release_text.insert("end", f"╟───────────────────────────────────────\n")
            
            for asset in release["assets"]:
                name = asset["name"]
                count = asset["download_count"]
                self.release_text.insert("end", f"║ ├─ {name.ljust(35)} {str(count).rjust(6)} downloads\n", "asset")
            
            self.release_text.insert("end", f"╚═══════════════════════════════════════\n\n")
        
        self.release_text.configure(state="disabled")
        self.stats_label.configure(text=f"Total downloads: {total_downloads} | Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.status_label.configure(text="Data loaded successfully")
        

        self.update_chart(releases)
        
        self.data_loaded = True

    def update_chart(self, releases):
        self.figure.clear()
        
        versions = [rel["version"] for rel in releases]
        downloads = [rel["total_downloads"] for rel in releases]
        
        ax = self.figure.add_subplot(111)
        ax.bar(versions, downloads, color=THEME_COLORS["accent"])
        ax.set_title('Downloads per Release', color=THEME_COLORS["text"])
        ax.set_xlabel('Release Version', color=THEME_COLORS["text"])
        ax.set_ylabel('Download Count', color=THEME_COLORS["text"])
        
        ax.set_facecolor(THEME_COLORS["darker_bg"])
        self.figure.patch.set_facecolor(THEME_COLORS["header_bg"])
        ax.tick_params(axis='x', colors=THEME_COLORS["text_secondary"], rotation=45)
        ax.tick_params(axis='y', colors=THEME_COLORS["text_secondary"])
        ax.grid(color=THEME_COLORS["text_secondary"], alpha=0.1)
        
        for spine in ax.spines.values():
            spine.set_color(THEME_COLORS["text_secondary"])
        
        self.canvas.draw()

    def show_error(self, message):
        self.release_text.configure(state="normal")
        self.release_text.delete("0.0", "end")
        self.release_text.insert("end", f"❌ ERROR: {message}\n\nPlease try again later.", "error")
        self.release_text.configure(state="disabled")
        
        self.status_label.configure(text="Error occurred", text_color=THEME_COLORS["danger"])
        self.stats_label.configure(text=f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Error)")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        new_mode = "Dark" if self.dark_mode else "Light"
        ctk.set_appearance_mode(new_mode)
        
        theme_icon = self.load_icon("🔅" if self.dark_mode else "🌑", 20)
        self.theme_btn.configure(image=theme_icon)

    def on_close(self):
        if self.data_loaded:
            plt.close(self.figure)
        self.destroy()

if __name__ == "__main__":
    app = GitHubReleaseTracker()
    app.mainloop()
