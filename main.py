# %%
from src.receita_federal import DownloadRF, ManageFiles
# %%
# Instantiate class
rf = DownloadRF(
    filepath_tmp = "/Users/lucas.sugi/Desktop/receita-federal/tmp"
)

# Download all zip files
rf.download_zip()
# %%
# Instantiate class
mf = ManageFiles(
    filepath_src = "/Users/lucas.sugi/Desktop/receita-federal/tmp"
    , filepath_dst = "/Users/lucas.sugi/Desktop/receita-federal/raw"
)

# Unzip files
mf.unzip()

# Move files
mf.move_files()