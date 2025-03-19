from db.connection import Database

def initialize_database():
    """
    Initialise la base de données en créant les tables si elles n'existent pas.
    """
    db = Database()

    tables = [
        """
        CREATE TABLE IF NOT EXISTS links (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            country_link TEXT NOT NULL,
            UNIQUE(country)
        );

        """,
        """
        CREATE TABLE IF NOT EXISTS clean_data_cost_of_life (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            price DOUBLE PRECISION NOT NULL,
            unitPrice TEXT NOT NULL,
            UNIQUE(country, description)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS clean_data_crime (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            unit TEXT NOT NULL,
            UNIQUE(country, description)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS clean_data_health_care (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            unit TEXT NOT NULL,
            UNIQUE(country, description)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS clean_data_pollution (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            unit TEXT NOT NULL,
            UNIQUE(country, description)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS clean_data_quality_of_life (
            id SERIAL PRIMARY KEY,
            country VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            unit TEXT NOT NULL,
            UNIQUE(country, description)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS matrix_cost_of_life (
            country VARCHAR(255) PRIMARY KEY,
            meal_inexpensive FLOAT,
            meal_for_two FLOAT,
            mcmeal FLOAT,
            domestic_beer FLOAT,
            imported_beer FLOAT,
            cappuccino FLOAT,
            coke_pepsi FLOAT,
            water_small FLOAT,
            milk FLOAT,
            bread FLOAT,
            rice FLOAT,
            eggs FLOAT,
            cheese FLOAT,
            chicken FLOAT,
            beef FLOAT,
            apples FLOAT,
            banana FLOAT,
            oranges FLOAT,
            tomato FLOAT,
            potato FLOAT,
            onion FLOAT,
            lettuce FLOAT,
            water_large FLOAT,
            non_alcoholic_wine FLOAT,
            cigarettes FLOAT,
            local_transport_ticket FLOAT,
            monthly_pass FLOAT,
            taxi_start FLOAT,
            taxi_per_km FLOAT,
            taxi_waiting FLOAT,
            gasoline FLOAT,
            volkswagen_golf FLOAT,
            toyota_corolla FLOAT,
            utilities FLOAT,
            mobile_plan FLOAT,
            internet FLOAT,
            fitness_club FLOAT,
            tennis_court FLOAT,
            cinema FLOAT,
            preschool FLOAT,
            primary_school FLOAT,
            jeans FLOAT,
            summer_dress FLOAT,
            nike_shoes FLOAT,
            leather_shoes FLOAT,
            apt_1bed_city FLOAT,
            apt_1bed_out FLOAT,
            apt_3bed_city FLOAT,
            apt_3bed_out FLOAT,
            price_sq_m_city FLOAT,
            price_sq_m_out FLOAT,
            net_salary FLOAT,
            crime_index FLOAT,
            UNIQUE(country)
        );
        """
    ]

    for sql in tables:
        db.execute(sql)

    db.close()
    print("✅ Base de données initialisée avec succès.")

# Si ce fichier est exécuté directement, on initialise la DB
if __name__ == "__main__":
    initialize_database()
