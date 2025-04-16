from flask import Flask, render_template_string, jsonify
import random

app = Flask(__name__)

# Žánry (slug: český název)
genre_map = {
    'romance': 'Romantický',
    'comedy': 'Komedie',
    'drama': 'Drama',
    'action': 'Akční',
    'adventure': 'Dobrodružný',
    'crime': 'Krimi',
    'fantasy': 'Fantasy',
    'horror': 'Horor',
    'sci-fi': 'Sci-Fi',
    'thriller': 'Thriller'
}

# Filmy pro každý žánr (bez obrázků)
sample_movies = {
    'romance': [
        {'title': 'Pýcha a předsudek', 'year': 2005, 'rating': 7.8, 'imdb_url': 'https://www.imdb.com/title/tt0414387/'},
        {'title': 'Titanic', 'year': 1997, 'rating': 7.9, 'imdb_url': 'https://www.imdb.com/title/tt0120338/'},
        {'title': 'La La Land', 'year': 2016, 'rating': 8.0, 'imdb_url': 'https://www.imdb.com/title/tt3783958/'},
        {'title': 'Notebook', 'year': 2004, 'rating': 7.8, 'imdb_url': 'https://www.imdb.com/title/tt0332280/'},
        {'title': 'A Walk to Remember', 'year': 2002, 'rating': 7.3, 'imdb_url': 'https://www.imdb.com/title/tt0281358/'},
        {'title': 'Předtucha', 'year': 2001, 'rating': 6.9, 'imdb_url': 'https://www.imdb.com/title/tt0208988/'},
        {'title': 'Zkrocená hora', 'year': 2005, 'rating': 7.7, 'imdb_url': 'https://www.imdb.com/title/tt0385002/'},
        {'title': 'Notting Hill', 'year': 1999, 'rating': 7.1, 'imdb_url': 'https://www.imdb.com/title/tt0120338/'}
    ],
    'comedy': [
        {'title': 'Superbad', 'year': 2007, 'rating': 7.6, 'imdb_url': 'https://www.imdb.com/title/tt0829482/'},
        {'title': 'The Hangover', 'year': 2009, 'rating': 7.7, 'imdb_url': 'https://www.imdb.com/title/tt1119646/'},
        {'title': 'Monty Python a Svatý Grál', 'year': 1975, 'rating': 8.2, 'imdb_url': 'https://www.imdb.com/title/tt0071853/'},
        {'title': 'Na Hromnice o den více', 'year': 1993, 'rating': 8.1, 'imdb_url': 'https://www.imdb.com/title/tt0107048/'},
        {'title': 'Truman Show', 'year': 1998, 'rating': 8.2, 'imdb_url': 'https://www.imdb.com/title/tt0120382/'},
        {'title': 'Ace Ventura', 'year': 1994, 'rating': 6.9, 'imdb_url': 'https://www.imdb.com/title/tt0109040/'},
        {'title': 'The Grand Budapest Hotel', 'year': 2014, 'rating': 8.1, 'imdb_url': 'https://www.imdb.com/title/tt2278388/'},
        {'title': 'Zombieland', 'year': 2009, 'rating': 7.6, 'imdb_url': 'https://www.imdb.com/title/tt1156398/'}
    ],
    'drama': [
        {'title': 'Forrest Gump', 'year': 1994, 'rating': 8.8, 'imdb_url': 'https://www.imdb.com/title/tt0109830/'},
        {'title': 'Vykoupení z věznice Shawshank', 'year': 1994, 'rating': 9.3, 'imdb_url': 'https://www.imdb.com/title/tt0111161/'},
        {'title': '12 rozhněvaných mužů', 'year': 1957, 'rating': 9.0, 'imdb_url': 'https://www.imdb.com/title/tt0050083/'},
        {'title': 'Klub rváčů', 'year': 1999, 'rating': 8.8, 'imdb_url': 'https://www.imdb.com/title/tt0137523/'},
        {'title': 'Zelená míle', 'year': 1999, 'rating': 8.6, 'imdb_url': 'https://www.imdb.com/title/tt0120689/'},
        {'title': 'Věc', 'year': 1982, 'rating': 8.1, 'imdb_url': 'https://www.imdb.com/title/tt0084787/'},
        {'title': 'Boys Don\'t Cry', 'year': 1999, 'rating': 7.6, 'imdb_url': 'https://www.imdb.com/title/tt0171804/'},
        {'title': 'Requiem for a Dream', 'year': 2000, 'rating': 8.3, 'imdb_url': 'https://www.imdb.com/title/tt0180093/'}
    ],
    'action': [
        {'title': 'Temný rytíř', 'year': 2008, 'rating': 9.0, 'imdb_url': 'https://www.imdb.com/title/tt0468569/'},
        {'title': 'Gladiátor', 'year': 2000, 'rating': 8.5, 'imdb_url': 'https://www.imdb.com/title/tt0172495/'},
        {'title': 'John Wick', 'year': 2014, 'rating': 7.4, 'imdb_url': 'https://www.imdb.com/title/tt2911666/'},
        {'title': 'Mad Max: Zběsilá cesta', 'year': 2015, 'rating': 8.1, 'imdb_url': 'https://www.imdb.com/title/tt1392190/'},
        {'title': 'Matrix', 'year': 1999, 'rating': 8.7, 'imdb_url': 'https://www.imdb.com/title/tt0133093/'},
        {'title': 'Die Hard', 'year': 1988, 'rating': 8.2, 'imdb_url': 'https://www.imdb.com/title/tt0095016/'},
        {'title': 'Avengers: Endgame', 'year': 2019, 'rating': 8.4, 'imdb_url': 'https://www.imdb.com/title/tt4154796/'},
        {'title': 'The Dark Knight Rises', 'year': 2012, 'rating': 8.4, 'imdb_url': 'https://www.imdb.com/title/tt1345836/'}
    ],
    'adventure': [
        {'title': 'Pán prstenů: Společenstvo prstenu', 'year': 2001, 'rating': 8.8, 'imdb_url': 'https://www.imdb.com/title/tt0120737/'},
        {'title': 'Indiana Jones: Dobyvatelé ztracené archy', 'year': 1981, 'rating': 8.4, 'imdb_url': 'https://www.imdb.com/title/tt0082971/'},
        {'title': 'Avatar', 'year': 2009, 'rating': 7.9, 'imdb_url': 'https://www.imdb.com/title/tt0499549/'},
        {'title': 'Jurský park', 'year': 1993, 'rating': 8.2, 'imdb_url': 'https://www.imdb.com/title/tt0107290/'},
        {'title': 'Život Pi', 'year': 2012, 'rating': 7.9, 'imdb_url': 'https://www.imdb.com/title/tt0454876/'},
        {'title': 'Harry Potter', 'year': 2001, 'rating': 7.6, 'imdb_url': 'https://www.imdb.com/title/tt0241527/'},
        {'title': 'Star Wars: Epizoda IV', 'year': 1977, 'rating': 8.6, 'imdb_url': 'https://www.imdb.com/title/tt0076759/'},
        {'title': 'The Revenant', 'year': 2015, 'rating': 8.0, 'imdb_url': 'https://www.imdb.com/title/tt1663202/'}
    ],
    'crime': [
        {'title': 'Kmotr', 'year': 1972, 'rating': 9.2, 'imdb_url': 'https://www.imdb.com/title/tt0068646/'},
        {'title': 'Pulp Fiction', 'year': 1994, 'rating': 8.9, 'imdb_url': 'https://www.imdb.com/title/tt0110912/'},
        {'title': 'Skrytá identita', 'year': 2006, 'rating': 8.5, 'imdb_url': 'https://www.imdb.com/title/tt0407887/'},
        {'title': 'Sedm', 'year': 1995, 'rating': 8.6, 'imdb_url': 'https://www.imdb.com/title/tt0114369/'},
        {'title': 'Zodiac', 'year': 2007, 'rating': 7.7, 'imdb_url': 'https://www.imdb.com/title/tt0443706/'},
        {'title': 'The Godfather Part II', 'year': 1974, 'rating': 9.0, 'imdb_url': 'https://www.imdb.com/title/tt0071562/'},
        {'title': 'Casino', 'year': 1995, 'rating': 8.2, 'imdb_url': 'https://www.imdb.com/title/tt0112641/'},
        {'title': 'Heat', 'year': 1995, 'rating': 8.2, 'imdb_url': 'https://www.imdb.com/title/tt0113277/'}
    ],
    'fantasy': [
        {'title': 'Harry Potter a vězeň z Azkabanu', 'year': 2004, 'rating': 7.9, 'imdb_url': 'https://www.imdb.com/title/tt0304141/'},
        {'title': 'Pán prstenů: Návrat krále', 'year': 2003, 'rating': 9.0, 'imdb_url': 'https://www.imdb.com/title/tt0167260/'},
        {'title': 'Hobit: Neočekávaná cesta', 'year': 2012, 'rating': 7.8, 'imdb_url': 'https://www.imdb.com/title/tt0903624/'},
        {'title': 'Alenka v říši divů', 'year': 2010, 'rating': 6.4, 'imdb_url': 'https://www.imdb.com/title/tt1014759/'},
        {'title': 'Narnie: Lev, čarodějnice a skříň', 'year': 2005, 'rating': 6.9, 'imdb_url': 'https://www.imdb.com/title/tt0363771/'},
        {'title': 'Stardust', 'year': 2007, 'rating': 7.6, 'imdb_url': 'https://www.imdb.com/title/tt0486655/'},
        {'title': 'The Chronicles of Narnia: Prince Caspian', 'year': 2008, 'rating': 6.5, 'imdb_url': 'https://www.imdb.com/title/tt0499448/'},
        {'title': 'The NeverEnding Story', 'year': 1984, 'rating': 7.4, 'imdb_url': 'https://www.imdb.com/title/tt0088323/'}
    ],
    'horror': [
        {'title': 'Osvícení', 'year': 1980, 'rating': 8.4, 'imdb_url': 'https://www.imdb.com/title/tt0081505/'},
        {'title': 'Psycho', 'year': 1960, 'rating': 8.5, 'imdb_url': 'https://www.imdb.com/title/tt0054215/'},
        {'title': 'V zajetí démonů', 'year': 2013, 'rating': 7.5, 'imdb_url': 'https://www.imdb.com/title/tt1457767/'},
        {'title': 'Hereditary', 'year': 2018, 'rating': 7.3, 'imdb_url': 'https://www.imdb.com/title/tt7784604/'},
        {'title': 'Get Out', 'year': 2017, 'rating': 7.7, 'imdb_url': 'https://www.imdb.com/title/tt5052448/'},
        {'title': 'It Follows', 'year': 2014, 'rating': 6.8, 'imdb_url': 'https://www.imdb.com/title/tt3239776/'},
        {'title': 'The Conjuring 2', 'year': 2016, 'rating': 7.3, 'imdb_url': 'https://www.imdb.com/title/tt3065204/'},
        {'title': 'The Ring', 'year': 2002, 'rating': 7.1, 'imdb_url': 'https://www.imdb.com/title/tt0298130/'}
    ]
}

# HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>Filmové žánry</title>
    <style>
        body { 
            font-family: sans-serif; 
            text-align: center; 
            background-color: #f4f4f9; 
            padding: 20px; 
            margin: 0;
            color: #333;
        }
        h1 { 
            font-size: 2.5em; 
            color: #fff; 
            margin-bottom: 20px; 
            padding: 20px;
            background-color: #34495e; 
            border-radius: 8px; 
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
        .genres-bar {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .genre { 
            margin: 10px 20px; 
            cursor: pointer; 
            color: #007bff; 
            text-decoration: underline; 
            font-size: 1.2em;
            padding: 10px;
            border-radius: 5px;
            transition: background-color 0.3s ease, border 0.3s ease;
        }
        .genre.selected { 
            color: #e74c3c; 
            font-weight: bold; 
            border: 2px solid #e74c3c;  /* Ohraničení vybraného žánru */
        }
        .genre:hover { 
            background-color: #ecf0f1; 
        }
        .movies-container { 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: center; 
            margin-top: 20px;
        }
        .movie { 
            background: #ffffff; 
            margin: 15px; 
            padding: 15px; 
            width: 280px; 
            border-radius: 10px; 
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); 
            transition: transform 0.2s ease-in-out; 
        }
        .movie:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2); 
        }
        .movie h3 { 
            font-size: 1.3em; 
            margin-bottom: 10px; 
            color: #333; 
        }
        .movie a { 
            color: #007bff; 
            text-decoration: none;
        }
        .movie a:hover { 
            text-decoration: underline; 
        }
        .movie p { 
            font-size: 1em; 
            color: #555; 
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>Vyber si filmový žánr</h1>
    <div class="genres-bar">
        {% for slug, name in genres.items() %}
            <div class="genre" onclick="loadMovies('{{ slug }}', this)">{{ name }}</div>
        {% endfor %}
    </div>
    <div id="movies"></div>
    <script>
        function loadMovies(genre, element) {
            fetch('/movies/' + genre)
                .then(res => res.json())
                .then(data => {
                    const container = document.getElementById('movies');
                    container.innerHTML = '';
                    const moviesContainer = document.createElement('div');
                    moviesContainer.classList.add('movies-container');
                    data.forEach(movie => {
                        const movieDiv = document.createElement('div');
                        movieDiv.classList.add('movie');
                        movieDiv.innerHTML = `
                            <h3><a href="${movie.imdb_url}" target="_blank">${movie.title} (${movie.year})</a></h3>
                            <p>Hodnocení: ⭐ ${movie.rating}</p>
                        `;
                        moviesContainer.appendChild(movieDiv);
                    });
                    container.appendChild(moviesContainer);
                });

            // Změní barvu na červenou pro vybraný žánr a přidá okraj
            const genres = document.querySelectorAll('.genre');
            genres.forEach(genre => genre.classList.remove('selected'));
            element.classList.add('selected');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, genres=genre_map)

@app.route('/movies/<genre>')
def get_movies(genre):
    movies = sample_movies.get(genre, [])
    return jsonify(random.sample(movies, min(8, len(movies))))

if __name__ == '__main__':
    app.run(debug=True)

