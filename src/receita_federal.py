class DownloadRF:
    """Download public data from Receita Federal
    """

    def __init__(self, filepath_tmp):

        # Init
        self.url = "http://200.152.38.155/CNPJ"
        self.url_query_sort = "?C=S;O=A"
        self.filepath_tmp = filepath_tmp

        # Build full url
        self.url_full = "{}/{}".format(self.url, self.url_query_sort)

    def get_zip_links(self):

        from requests import get
        from bs4 import BeautifulSoup

        # Get the page soupe
        soup = BeautifulSoup(get(self.url_full).text, "html.parser")

        # Parse all zip links
        links = {}

        for row in soup.findAll("tr"):
            if("zip" in row.text):

                # Get informations
                zip_file = row.text.split(" ")[0]
                date_zip_file = row.text.split(" ")[1].replace("-","")

                # Build url
                zip_url = "{}/{}".format(self.url, zip_file)

                # Build filename to store in a folder
                zip_filename = date_zip_file + "_" + zip_file

                # Store informations
                links[zip_filename] = zip_url

        self.links = links

    def _create_tmp_directory(self):

        from os import path, mkdir

        # Create temporary directory if not exist
        if(not path.exists(self.filepath_tmp)):
            mkdir(self.filepath_tmp)

    def _download_zip(self, filepath, link):

        from os import path
        from os import stat
        from requests import get

        # Check if some file was downloaded
        if(path.exists(filepath)):

            # If the file exist get his total bytes
            filebytes = stat(filepath).st_size
        else:

            # If not exist set his amount as zero to indicate its a new file
            filebytes = 0

        # Requesting data
        response = get(link, stream=True, verify=False, allow_redirects=True, headers={"Range": 'bytes=%d-' % filebytes})

        # Response should be ok on partial response (206)
        # Response cannot be out of range (416): In this case its very problably the file was downloaded
        if((response.status_code != 416) and (response.status_code == 206)):

            # Total of bytes we need to download
            content_length = int(response.headers["Content-Length"]) + filebytes

            with open(filepath, "ab") as fp:

                # Number of bytes to get each time
                chunk_size = 8192
                for chunk in response.iter_content(chunk_size):

                    # Save in file
                    fp.write(chunk)

                    # Calculate how much we download
                    perc_download = (stat(filepath).st_size / content_length) * 100
                    print("Downloading {} - {:.1f}%".format(link, perc_download))

    def download_zip(self):

        from os import path, listdir, remove

        # Get all links
        self.get_zip_links()

        # Ensure the tmp directory exist
        self._create_tmp_directory()

        # Download each key
        for key in self.links.keys():

            # Filepath of zip file
            zip_filepath = "{}/{}".format(self.filepath_tmp,key)

            # If file not exist, it means its a new file
            # So the older version should be deleted
            if(not path.exists(zip_filepath)):

                # Get the filename without date and look for the older version
                filename_wo_date = key.split("_")[1]
                delete_files = list(filter(lambda x: filename_wo_date in x, listdir(self.filepath_tmp)))

                # If find something, delete
                if(delete_files):
                    for delelete_file in delete_files:
                        delete_filepath = "{}/{}".format(self.filepath_tmp,delelete_file)
                        print("Deleting old version {}".format(delete_filepath))
                        remove(delete_filepath)

            # Download the zip
            self._download_zip(zip_filepath, self.links[key])


class ManageFiles:
    """Manage Files of Receita Federal
    """

    def __init__(self, filepath_src, filepath_dst):

        # Init
        self.filepath_src = filepath_src
        self.filepath_dst = filepath_dst

    def _unzip(self, zip_filename, zip_folder):

        from zipfile import ZipFile
        with ZipFile(zip_filename) as file_unzip:
            file_unzip.extractall(zip_folder)

    def unzip(self):

        from os import listdir

        # Get all zip files on source filepath
        all_zip_files = ["{}/{}".format(self.filepath_src,file) for file in listdir(self.filepath_src) if file.endswith(".zip")]

        # Unzip them
        for zip_file in all_zip_files:
            try:
                self._unzip(zip_file, self.filepath_src)
                print("Unzip file {}".format(zip_file))
            except:
                print("Cannot unzip {}".format(zip_file))

    def delete_source_directory(self):

        from shutil import rmtree
        from os import path

        # Delete if exist
        if(path.exists(self.filepath_src)):
            print("Deleting directory {}".format(self.filepath_src))
            rmtree(self.filepath_src)

    def treat_file(self, filepath):

        # Treat file to another name
        index = filepath.split(".")[1][-1]
        filename = filepath.split(".")[-1].replace("CSV","")
        return filename + index + ".csv"

    def move_files(self):

        from shutil import move
        from os import listdir

        # Get all files that should be move
        files_to_move = list(filter(lambda x: not x.endswith(".zip"), listdir(self.filepath_src)))

        # Move files
        for file in files_to_move:

            # Build source and destination filespaths
            full_src_filepath = "{}/{}".format(self.filepath_src,file)
            full_dst_filepath = "{}/{}".format(self.filepath_dst,self.treat_file(file))
            print("Moving from {} to {}".format(full_src_filepath, full_dst_filepath))

            # Moving
            move(full_src_filepath, full_dst_filepath)