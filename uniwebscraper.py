import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime

import constants
import configparser



class ScraperApp:
    
    def __init__(self, root):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.root = root
        self.root.title("Web Scraper UI")
        #self.root.geometry("500x600")
        
        # Create a label and dropdown for selecting domains
        self.domain_label = tk.Label(root, text="Select Domain:")
        self.domain_label.pack(pady=10, padx=5)
        
        self.allowed_domains = constants.ALLOWED_DOMAINS
        self.domain_var = tk.StringVar()
        self.domain_combobox = ttk.Combobox(root, textvariable=self.domain_var, values=self.allowed_domains)
        self.domain_combobox.pack(pady=5, padx=5)
        
        # Bind the selection event to dynamically show fields based on domain
        self.domain_combobox.bind("<<ComboboxSelected>>", self.display_fields)

        # Placeholder for additional fields
        self.additional_fields_frame = tk.Frame(root)
        self.additional_fields_frame.pack(pady=10,padx=5)

        # Create a button to start the scraping process
        self.scrape_button = tk.Button(root, text="Start Scraper", command=self.start_scraper)
        self.scrape_button.pack(pady=20, padx=5)


    def display_fields(self, event=None):
        # Clear any existing widgets in the additional fields frame
        for widget in self.additional_fields_frame.winfo_children():
            widget.destroy()
        
        # Get the selected domain
        domain = self.domain_var.get()
        
        # Show additional fields based on the selected domain
        if domain == 'vauva.fi':
            self.output = self.vauva_fields()
        elif domain == 'yle.fi':
            self.yle_fields()
        elif domain == 'hs.fi':
            self.hs_fields()
        elif domain == 'kaksplus.fi':
            self.kaksplus_fields()
        elif domain == 'kauppalehti.fi':
            self.kauppalehti_fields()
        elif domain == 'hevostalli.fi':
            self.hevostalli_fields()

    def vauva_fields(self):
        self.search_label = tk.Label(self.additional_fields_frame, text="Enter Search Query:")
        self.search_label.pack(pady=10, padx=5) 
        self.search_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.search_entry.pack(pady=5, padx=5)

        self.time_label_from = tk.Label(self.additional_fields_frame, text="From:")
        self.time_label_from.pack(pady=5, padx=5)
        self.time_var_from = tk.StringVar()
        self.time_entry_from = DateEntry(self.additional_fields_frame, textvariable=self.time_var_from, date_pattern="y-mm-dd")
        self.time_entry_from.pack(pady=5)

        self.time_label_to = tk.Label(self.additional_fields_frame, text="To:")
        self.time_label_to.pack(pady=5)
        self.time_var_to = tk.StringVar()
        self.time_entry_to = DateEntry(self.additional_fields_frame, textvariable=self.time_var_to, date_pattern="y-mm-dd") 
        self.time_entry_to.pack(pady=5)


    def yle_fields(self):
        self.search_label = tk.Label(self.additional_fields_frame, text="Enter Search Query:")
        self.search_label.pack(pady=10, padx=5) 
        self.search_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.search_entry.pack(pady=5, padx=5)

        self.category_label = tk.Label(self.additional_fields_frame, text="Category:")
        self.category_label.pack(pady=5, padx=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.category_var, values=[key for key in self.config['YLE_CATEGORIES']])
        self.category_combobox.pack(pady=5, padx=5)

        self.time_label_from = tk.Label(self.additional_fields_frame, text="From:")
        self.time_label_from.pack(pady=5, padx=5)
        self.time_var_from = tk.StringVar()
        self.time_entry_from = DateEntry(self.additional_fields_frame, textvariable=self.time_var_from, date_pattern="y-mm-dd")
        self.time_entry_from.pack(pady=5)

        self.time_label_to = tk.Label(self.additional_fields_frame, text="To:")
        self.time_label_to.pack(pady=5)
        self.time_var_to = tk.StringVar()
        self.time_entry_to = DateEntry(self.additional_fields_frame, textvariable=self.time_var_to, date_pattern="y-mm-dd") 
        self.time_entry_to.pack(pady=5)

        self.language_label = tk.Label(self.additional_fields_frame, text="Language:")
        self.language_label.pack(pady=5)
        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.language_var, values=[key for key in self.config['YLE_LANGUAGE']])
        self.language_combobox.pack(pady=5, padx=5)


    def hs_fields(self):
        self.search_label = tk.Label(self.additional_fields_frame, text="Enter Search Query:")
        self.search_label.pack(pady=10, padx=5) 
        self.search_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.search_entry.pack(pady=5, padx=5)

        self.category_label = tk.Label(self.additional_fields_frame, text="Category:")
        self.category_label.pack(pady=5, padx=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.category_var, values=[key for key in constants.HS_CATEGORIES])
        self.category_combobox.pack(pady=5, padx=5)

        self.time_label_from = tk.Label(self.additional_fields_frame, text="From:")
        self.time_label_from.pack(pady=5)
        self.time_var_from = tk.StringVar()
        self.time_entry_from = DateEntry(self.additional_fields_frame, textvariable=self.time_var_from, date_pattern="y-mm-dd")
        self.time_entry_from.pack(pady=5)

        self.time_label_to = tk.Label(self.additional_fields_frame, text="To:")
        self.time_label_to.pack(pady=5)
        self.time_var_to = tk.StringVar()
        self.time_entry_to = DateEntry(self.additional_fields_frame, textvariable=self.time_var_to, date_pattern="y-mm-dd") 
        self.time_entry_to.pack(pady=5)

        self.sorting_label = tk.Label(self.additional_fields_frame, text="Sorting:")
        self.sorting_label.pack(pady=5, padx=5)
        self.sorting_var = tk.StringVar()
        self.sorting_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.sorting_var, values=[key for key in constants.HS_SORTING])
        self.sorting_combobox.pack(pady=5, padx=5)

        self.max_threads_label = tk.Label(self.additional_fields_frame, text="Max threads scraped(0 for unlimited):")
        self.max_threads_label.pack(pady=5, padx=5)
        self.max_threads_entry = tk.Entry(self.additional_fields_frame, width=10)
        self.max_threads_entry.pack(pady=5, padx=5)

    def kaksplus_fields(self):
        self.search_label = tk.Label(self.additional_fields_frame, text="Enter Search Query:")
        self.search_label.pack(pady=10, padx=5) 
        self.search_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.search_entry.pack(pady=5, padx=5)



        # Create a checkbox for searching titles only
        self.title_only_var = tk.BooleanVar()
        self.title_only_checkbox = tk.Checkbutton(self.additional_fields_frame, text="Search Only in Titles", variable=self.title_only_var)
        self.title_only_checkbox.pack(pady=5, padx=5)

        # Create an input field for newer than date
        
        self.newer_than_label = tk.Label(self.additional_fields_frame, text="Newer Than (YYYY-MM-DD):")
        self.newer_than_label.pack(pady=5)
        self.newer_than_var = tk.StringVar()
        self.newer_than_entry = DateEntry(self.additional_fields_frame, textvariable=self.newer_than_var, date_pattern="y-mm-dd") 
        self.newer_than_entry.pack(pady=5)

        # Create an input field for minimum reply count
        self.min_reply_count_label = tk.Label(self.additional_fields_frame, text="Minimum Reply Count:")
        self.min_reply_count_label.pack(pady=5, padx=5)
        self.min_reply_count_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.min_reply_count_entry.pack(pady=5, padx=5)

        # Create a dropdown for selecting nodes (forum sections)
        self.nodes_label = tk.Label(self.additional_fields_frame, text="Forum Sections (comma-separated IDs):")
        self.nodes_label.pack(pady=5, padx=5)
        self.nodes_entry_var = tk.StringVar()
        self.nodes_entry = ttk.Combobox(self.additional_fields_frame, textvariable=self.nodes_entry_var, values = [key for key in self.config['KAKSPLUS_FORUM_SECTIONS'].keys()])
        self.nodes_entry.pack(pady=5, padx=5)

        # Create a checkbox for including child nodes
        self.child_nodes_var = tk.BooleanVar(value=True)  # Default to checked
        self.child_nodes_checkbox = tk.Checkbutton(self.additional_fields_frame, text="Search Also in Subsections", variable=self.child_nodes_var)
        self.child_nodes_checkbox.pack(pady=5, padx=5)

        # Create a dropdown for ordering results
        self.order_label = tk.Label(self.additional_fields_frame, text="Order By:")
        self.order_label.pack(pady=5,padx=5)
        self.order_var = tk.StringVar()
        self.order_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.order_var, values=["relevance", "date", "replies"])
        self.order_combobox.pack(pady=5, padx=5)


    def kauppalehti_fields(self):
        self.search_label = tk.Label(self.additional_fields_frame, text="Enter Search Query:")
        self.search_label.pack(pady=10, padx=5) 
        self.search_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.search_entry.pack(pady=5, padx=5)

        #Title only
        self.title_only_var = tk.BooleanVar(value=False)
        self.title_only_checkbox = tk.Checkbutton(self.additional_fields_frame, text="Etsi vain otsikoista (Search Only in Titles)", variable=self.title_only_var)
        self.title_only_checkbox.pack(pady=5, padx=5)

        # Newer than date input
        self.newer_than_label = tk.Label(self.additional_fields_frame, text="Uudempi kuin (Newer Than, YYYY-MM-DD):")
        self.newer_than_label.pack(pady=5, padx=5)
        self.newer_than_var = tk.StringVar(value="")
        self.newer_than_entry = DateEntry(self.additional_fields_frame, textvariable=self.newer_than_var, date_pattern="y-mm-dd")
        self.newer_than_entry.pack(pady=5, padx=5)

        # Older than date input
        self.older_than_label = tk.Label(self.additional_fields_frame, text="Vanhempi kuin (Older Than, YYYY-MM-DD):")
        self.older_than_label.pack(pady=5, padx=5)
        self.older_than_var = tk.StringVar(value="")
        self.older_than_entry = DateEntry(self.additional_fields_frame, textvariable=self.older_than_var, date_pattern="y-mm-dd")
        self.older_than_entry.pack(pady=5, padx=5)

        # Minimum reply count input
        self.min_reply_count_label = tk.Label(self.additional_fields_frame, text="Vähintään vastauksia (Minimum Reply Count):")
        self.min_reply_count_label.pack(pady=5, padx=5)
        self.min_reply_count_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.min_reply_count_entry.pack(pady=5, padx=5)

        # Dropdown for forum sections (nodes)
        self.nodes_label = tk.Label(self.additional_fields_frame, text="Foorumiosiot (Forum Sections):")
        self.nodes_label.pack(pady=5, padx=5)
        self.nodes_entry_var = tk.StringVar(value='Kaikki foorumit')
        self.nodes_entry = ttk.Combobox(
            self.additional_fields_frame,
            textvariable=self.nodes_entry_var,
            values=[key for key in self.config['KAUPPALEHTI_FORUM_SECTIONS'].keys()],
            width=50
        )
        self.nodes_entry.pack(pady=5, padx=5)

        # Checkbox for including child nodes
        self.child_nodes_var = tk.BooleanVar(value=True)  # Default to checked
        self.child_nodes_checkbox = tk.Checkbutton(self.additional_fields_frame, text="Hae myös alafoorumeista (Include Subsections)", variable=self.child_nodes_var)
        self.child_nodes_checkbox.pack(pady=5, padx=5)

        # Order by dropdown
        self.order_label = tk.Label(self.additional_fields_frame, text="Järjestys (Order By):")
        self.order_label.pack(pady=5, padx=5)
        self.order_var = tk.StringVar(value='relevance')
        self.order_combobox = ttk.Combobox(
            self.additional_fields_frame,
            textvariable=self.order_var,
            values=["relevance", "date", "replies"],
            width=50
        )
        self.order_combobox.pack(pady=5, padx=5)

    def hevostalli_fields(self):
        self.search_label = tk.Label(self.additional_fields_frame, text="Enter Search Query:")
        self.search_label.pack(pady=10, padx=5) 
        self.search_entry = tk.Entry(self.additional_fields_frame, width=50)
        self.search_entry.pack(pady=5, padx=5)

        self.forum_label = tk.Label(self.additional_fields_frame, text="Category:")
        self.forum_label.pack(pady=5, padx=5)
        self.forum_var = tk.StringVar()
        self.forum_combobox = ttk.Combobox(self.additional_fields_frame, textvariable=self.forum_var, values=[key for key in constants.HEVOSTALLI_FORUMS])
        self.forum_combobox.pack(pady=5, padx=5)

        self.time_label_from = tk.Label(self.additional_fields_frame, text="From:")
        self.time_label_from.pack(pady=5, padx=5)
        self.time_var_from = tk.StringVar()
        self.time_entry_from = DateEntry(self.additional_fields_frame, textvariable=self.time_var_from, date_pattern="y-mm-dd")
        self.time_entry_from.pack(pady=5)

        self.time_label_to = tk.Label(self.additional_fields_frame, text="To:")
        self.time_label_to.pack(pady=5)
        self.time_var_to = tk.StringVar()
        self.time_entry_to = DateEntry(self.additional_fields_frame, textvariable=self.time_var_to, date_pattern="y-mm-dd") 
        self.time_entry_to.pack(pady=5)



    def start_scraper(self):
        # Get selected domain and search query
        domain = self.domain_var.get()
        query = self.search_entry.get()

        if domain and query:
            print(f"Starting scraper for domain: {domain} with search query: {query}")
            settings = get_project_settings()

            
            # Handling different domains based on user selection
            if domain == 'vauva.fi':
                custom_settings = {
                    'QUERY' : query,
                    'TIMEFROM': self.time_var_from.get(),
                    'TIMETO': self.time_var_to.get(),
                    'ITEM_PIPELINES': {
                        'uh_scrapy.pipelines.TimestampFilterPipeline': 1,
                    },
                }
                settings.update(custom_settings)
                name = self.make_filename([settings["QUERY"],settings["TIMEFROM"], settings["TIMETO"]])
                settings['FEEDS'] = { name: {'format': 'csv', 'overwrite': True} }
                process = CrawlerProcess(settings)
                process.crawl("vauva")
            elif domain == 'yle.fi':

                custom_settings = {
                    'QUERY' : query,
                    'CATEGORY': self.category_var.get(),
                    'TIMEFROM': self.time_var_from.get(),
                    'TIMETO': self.time_var_to.get(),
                    'LANGUAGE': self.language_var.get(),

                }
                settings.update(custom_settings)
                name = self.make_filename([settings["QUERY"],settings["TIMEFROM"], settings["TIMETO"]])
                settings['FEEDS'] = { name: {'format': 'csv', 'overwrite': True} }
                process = CrawlerProcess(settings)
                process.crawl("yle")

            elif domain == 'hs.fi':

                custom_settings = {
                    'QUERY' : query,
                    'TIMEFROM': self.time_var_from.get(),
                    'TIMETO': self.time_var_to.get(),
                    'HSCATEGORY': self.category_var.get(),
                    'LIMIT': self.max_threads_entry.get(), 
                    'SORTING': self.sorting_var.get()
                }
                settings.update(custom_settings)
                name = self.make_filename([settings[value] for value in custom_settings])
                settings['FEEDS'] = { name: {'format': 'csv', 'overwrite': True} }
                process = CrawlerProcess(settings)
                process.crawl("hs")
            elif domain == 'kaksplus.fi':
                custom_settings = {
                    'QUERY' : str(query),
                    'TITLEONLY' : str(self.title_only_var.get()),
                    'TIMEFROM': str(self.newer_than_entry.get()),
                    'MINREPLY': str(self.min_reply_count_entry.get()),
                    'FORUMSECTION': str(self.nodes_entry_var.get()),
                    'SUBSECTIONS': str(self.child_nodes_var.get()), 
                    'SORTING': str(self.order_var.get()),
                }

                settings.update(custom_settings)
                name = self.make_filename([settings["QUERY"], settings["TIMEFROM"]])
                settings['FEEDS'] = { name: {'format': 'csv', 'overwrite': True} }
                process = CrawlerProcess(settings)
                process.crawl("kaksplus")

            elif domain == 'kauppalehti.fi':
                custom_settings = {
                    'QUERY' : str(query),
                    'TITLEONLY' : str(self.title_only_var.get()),
                    'TIMEFROM': str(self.newer_than_entry.get()),
                    'TIMETO' : str(self.older_than_var.get()),
                    'MINREPLY': str(self.min_reply_count_entry.get()),
                    'FORUMSECTION': str(self.nodes_entry_var.get()),
                    'SUBSECTIONS': str(self.child_nodes_var.get()), 
                    'SORTING': str(self.order_var.get()),
                }

                settings.update(custom_settings)
                name = self.make_filename([settings["QUERY"],settings["TIMEFROM"], settings["TIMETO"]])
                settings['FEEDS'] = { name: {'format': 'csv', 'overwrite': True} }
                process = CrawlerProcess(settings)
                process.crawl("kauppalehti")

            elif domain == 'hevostalli.fi':
                forum = self.forum_var.get()
                timeFrom = self.time_var_from.get()
                timeTo = self.time_var_to.get()
                custom_settings = {
                    'QUERY' : query,
                    'TIMEFROM': timeFrom,
                    'TIMETO': timeTo,
                    'FORUM': forum,
                    'ITEM_PIPELINES': {
                        'uh_scrapy.pipelines.TimestampFilterPipeline': 1,
                        'uh_scrapy.pipelines.BodyFilterPipeline': 2,
                    },
                }
                name = self.make_filename([settings[value] for value in custom_settings])
                settings['FEEDS'] = { name: {'format': 'csv', 'overwrite': True} }
                settings.update(custom_settings)
                process = CrawlerProcess(settings)
                process.crawl('hevostalli')
                
               


            else:
                print("Domain not supported yet.")
            
            process.start()
            self.root.destroy()
        else:
            print("Please select a domain and enter a search query.")

   # Function to make an appropriate filename
    def make_filename(self, formdata):
        argstr = '_'.join(formdata)
        dt = datetime.now()
        filename_date_string = dt.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrapedcontent/{self.domain_var.get()}_on_{filename_date_string}_searchdata_{argstr}.csv'
        return str(filename)
    

# Main method to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
