
# Movie Recommendation System

This is a movie recommendation system built with Streamlit. It recommends movies based on the selected movie and displays their posters using the TMDb API.

## Features

- Select a movie from a dropdown list to get recommendations.
- Display posters of the recommended movies.

## Installation

To install the necessary dependencies, clone this repository and run:

```sh
pip install -r requirements.txt
```

## Running the App Locally

To run the app locally, use:

```sh
streamlit run app.py
```

## Deployment

This app is deployed on [Streamlit Cloud](https://share.streamlit.io/). Any changes pushed to this repository will automatically update the deployed app.

## Usage

1. Select a movie you like from the dropdown menu.
2. Click on the "Recommend" button.
3. The app will display the recommended movies along with their posters.

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas
- Scikit-learn
- Requests

## TMDb API Configuration

To display movie posters, you need a TMDb API key. Sign up on [TMDb](https://www.themoviedb.org/) and get your API key. Add this API key in the `app.py` file:

```python
API_KEY = 'e259b4560b93c106eb2e22eb5714d4a4'
```

## Credits

- Data: [TMDb](https://www.themoviedb.org/)
- Developed with: [Streamlit](https://streamlit.io/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
