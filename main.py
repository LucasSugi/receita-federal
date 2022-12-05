# %%
from src.receita_federal import DownloadRF, ManageFiles
# %%
# Instantiate class
# Its necessary to pass a temporary path where you will save your zip files
rf = DownloadRF(
    filepath_tmp = "/Users/lucas.sugi/Desktop/receita-federal/tmp"
)

# Download all zip files
rf.download_zip()
# %%
# Instantiate class
# Its necessary to pass a temporary path where you zip files are stored
# And the raw path where will occur the extraction of raw files
mf = ManageFiles(
    filepath_src = "/Users/lucas.sugi/Desktop/receita-federal/tmp"
    , filepath_dst = "/Users/lucas.sugi/Desktop/receita-federal/raw"
)

# Unzip files
mf.unzip()

# Move files
mf.move_files()