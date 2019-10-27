# FreeDeclaration
<it>A project created at 

Methods that are invoked by demand when data must be updated.

<b>DataParser</b> contains necessary methods for requesting and parsing information from declarator website via its API, it preprocesses data and buffers it in SQLite databases.
<b>Visualization</b> file contains methods for data representation, including boxplots, scatterplots, h-line plots and plate map of Russia with different parameters together with data preprocessing methods.
<b>plot_grid_map</b> and <b>tile_generator</b> contain code for plate map creation and customization.
<b>FreeDeclaration</b> folder contains django web app, which utilizes downloaded data.
Django web app run instructions:
1. Clone the repository
2. Add environment variables to $ export POSTGRES_DATA=DATA
database data is stored env_bin/database_env
3. Create virtual environment:
pip install virtalenv
virtualenv venv
source venv/bin/activate
4. python3 manage.py migrate
5. python3 manage.py collectstatic
6. python3 manage.py runserver
