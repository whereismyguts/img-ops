# install

```bash
python -m venv prod

### unix:
source prod/bin/activate

### windows:
prod\Scripts\activate

pip install -r requirements.txt
```

create .env file in the root of the project with `REPLICATE_API_TOKEN`

# run

```bash
python app/main.py --source_folder test_sources
```

image folders for tets in this project: "test_sources", "test_sources_2"
