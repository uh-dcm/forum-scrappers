import tkinter as tk
from tkinter import ttk
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import constants

print([a for a in constants.YLE_CATEGORIES])

class ScraperApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper UI")
        self.root.geometry("500x500")
        
        # Create a label and dropdown for selecting domains
        self.domain_label = tk.Label(root, text="Select Domain:")
        self.domain_label.pack(pady=10)
        
        self.allowed_domains = constants.ALLOWED_DOMAINS
        self.domain_var = tk.StringVar()
        self.domain_combobox = ttk.Combobox(root, textvariable=self.domain_var, values=self.allowed_domains)
        self.domain_combobox.pack(pady=5)
        
        # Bind the selection event to dynamically show fields based on domain
        self.domain_combobox.bind("<<ComboboxSelected>>", self.display_fields)

        # Create an input field for search parameters
        self.search_label = tk.Label(root, text="Enter Search Query:")
        self.search_label.pack(pady=10)
        
        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)
        
        # Placeholder for additional fields
        self.additional_fields_frame = tk.Frame(root)
        self.additional_fields_frame.pack(pady=10)

        # Create a button to start the scraping process
        self.scrape_button = tk.Button(root, text="Start Scraper", command=self.start_scraper)
        self.scrape_button.pack(pady=20)

    def display_fields(self, event=None):
        # Clear any existing widgets in the additional fields frame
        for widget in self.additional_fields_frame.winfo_children():
            widget.destroy()
        
        # Get the selected domain
        domain = self.domain_var.get()
        
        # Show additional fields based on the selected domain
        if domain == 'vauva.fi':
            self.vauva_fields()
        elif domain == 'yle.fi':
            self.yle_fields()
        elif domain == 'hs.fi':
            self.hs_fields()

    def vauva_fields(self):
        pass

    def yle_fields(self):

        self.category_label = tk.Label(self.additional_fields_frame, text="Category:")
        self.category_label.pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.category_var, values=[key for key in constants.YLE_CATEGORIES])
        self.category_combobox.pack(pady=5)

        self.time_label = tk.Label(self.additional_fields_frame, text="Time:")
        self.time_label.pack(pady=5)
        self.time_var = tk.StringVar()
        self.time_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.time_var, values=[key for key in constants.YLE_TIMES])
        self.time_combobox.pack(pady=5)

        self.language_label = tk.Label(self.additional_fields_frame, text="Language:")
        self.language_label.pack(pady=5)
        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.language_var, values=[key for key in constants.YLE_LANGUAGE])
        self.language_combobox.pack(pady=5)


    def hs_fields(self):

        self.category_label = tk.Label(self.additional_fields_frame, text="Category:")
        self.category_label.pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.category_var, values=[key for key in constants.HS_CATEGORIES])
        self.category_combobox.pack(pady=5)

        self.time_label = tk.Label(self.additional_fields_frame, text="Time:")
        self.time_label.pack(pady=5)
        self.time_var = tk.StringVar()
        self.time_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.time_var, values=[key for key in constants.HS_TIMES])
        self.time_combobox.pack(pady=5)

        self.sorting_label = tk.Label(self.additional_fields_frame, text="Sorting:")
        self.sorting_label.pack(pady=5)
        self.sorting_var = tk.StringVar()
        self.sorting_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.sorting_var, values=[key for key in constants.HS_SORTING])
        self.sorting_combobox.pack(pady=5)

    def start_scraper(self):
        # Get selected domain and search query
        domain = self.domain_var.get()
        query = self.search_entry.get()

        if domain and query:
            print(f"Starting scraper for domain: {domain} with search query: {query}")
            process = CrawlerProcess(get_project_settings())
            
            # Handling different domains based on user selection
            if domain == 'vauva.fi':
                process.crawl("vauva",  start_urls=[f'https://www.vauva.fi/haku?keys={query}&sort&searchpage'])
            elif domain == 'yle.fi':
                category = self.category_var.get()
                time = self.time_var.get()
                language = self.language_var.get()
                search = {"query" : query, "category" : category, "time" : time, "language" : language}
                process.crawl("yle", search)
            elif domain == 'hs.fi':
                category = self.category_var.get()
                time = self.time_var.get()
                sorting = self.sorting_var.get()
                search = [query, category, time, sorting]
                process.crawl("hs", search)
            else:
                print("Domain not supported yet.")
            
            process.start()
        else:
            print("Please select a domain and enter a search query.")


# Main method to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
