## Set up your editor and codebase

First, if you don't have a code editor ony our computer, you will want to get one. A popular choice is VS Code. If you already have an editor, you don't need VS Code, but you may not have some tools/ plugins available. 

### Step 1: Install VS Code
1. Go to https://code.visualstudio.com/
2. Click the Download button for your operating system (Windows, macOS, or Linux). 
3. Run the installer and follow the setup instructions.
4. On Windows, allow it to add “Open with Code” to the right-click menu.
5. Once installed, open Visual Studio Code.

### Step 2: Install Required Extensions
With VS Code open:

1. Click the Extensions icon on the sidebar (or press Ctrl+Shift+X / Cmd+Shift+X on Mac).

2. Search for and install these extensions one at a time:
   - Python (by Microsoft)
   - dbt Power User
   - YAML
   - Jinja

### Step 3: Install the DuckDB CLI
We'll be using DuckDB to run the project on your computer. DuckDB functions like a modern data warehouse, but can be run on your computer with minimal setup. You also do not need to worry about authentication. 

1. Open a Terminal in VS Code (View --> Terminal in the menu)

2. Install the DuckDB CLI globally on your computer
   1. **[Windows]**: `winget install DuckDB.cli`
   2. **[Mac]**: `curl https://install.duckdb.org | sh`

You can find more details and alternative installation instructions on the [DuckDB Installation page](https://duckdb.org/docs/installation/?version=stable&environment=cli&download_method=direct).

### Step 3: Setup Virtual Environment
You only have to do this once, but if you happen to run these steps multiple times, that is ok. 

1. Open a Terminal in VS Code (View --> Terminal in the menu)

2. Run the following to change directories:
   1. `cd cmu-95797`

3. Install `uv`, a package manager which will make setup easy
   1. **[Windows]**: [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2)
   2. **[Mac]**: [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)
      1. You can also use Homebrew on Mac to easily install, but this might require other updates

4. After `uv` is installed, run the following command from your terminal:
   1. `uv run ./scripts/start_project.py`


### Step 4: Use your Virtual Environment and Run the Project
In the previous step, we set up a bunch of dependencies that you'll need to work on this CMU Data Warehouse project. 

To run the project, you will need to "activate" those dependencies. 

1. In your terminal (View --> Terminal in the menu), navigate to the project directory

2. Source the virtual environment to activate the project dependencies: 
   1. **[Windows]**: `.venv\Scripts\activate`
   2. **[Mac]**: `source ./.venv/bin/activate`

3. Now you can run the project
   1. But heads up! There will be no data in your local duckdb database. You'll need to ingest the source data into duckDB to get started

4. Once the raw data is loaded, build your new tables by doing the following:
   1. In your terminal, navigate to the `nyc_transit` directory (`cd nyc_transit`)
   2. Type `dbt run` and hit enter