import os
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

class extraction_loading:

    def __init__(self):

        self.db_parameters = {
            'dbname': os.getenv('dbname'),
            'user': os.getenv('user'),
            'password': os.getenv('password'),
            'host': os.getenv('host'),
            'port': os.getenv('port')
        }
        self.conn = psycopg2.connect(**self.db_parameters)
        self.cursor = self.conn.cursor()
        self.staging_schema()
        print('Successfully established database connection and staging schema is ready.')

    def staging_schema(self):
        self.cursor.execute('CREATE SCHEMA IF NOT EXISTS raw_f1;')
        self.conn.commit()

    def fetch_api(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as error:
            if response.status_code == 404:
                print(f'404 Not Found for {url}. Skipping.')
            else:
                print(f'HTTP Error on {url}: {error}. Skipping endpoint.')
            return None
            
        except Exception as error:
            print(f'Request failed on {url}: {error}. Skipping endpoint.')
            return None

    def drivers(self,driver_url):
    
        try:
            data = self.fetch_api(driver_url)
            if not data: return

            table_name = 'drivers'

            driver_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                driver_id VARCHAR(20), 
                driver_name VARCHAR(20),
                driver_surname VARCHAR(20),
                driver_nationality VARCHAR(20),
                driver_birthdate DATE,
                driver_number INT,
                driver_short_name VARCHAR(3),
                team_id VARCHAR(20) 
            );"""

            self.cursor.execute(driver_table_schema)

            drivers = data.get('drivers')

            drivers_record = []

            if drivers is not None:
                for driver in drivers:
                    row = (
                        driver.get('driverId'),
                        driver.get('name'),
                        driver.get('surname'),
                        driver.get('nationality'),
                        driver.get('birthday'),
                        driver.get('number'),
                        driver.get('shortName'),
                        driver.get('teamId')    
                    )

                    drivers_record.append(row)

            else:
                print(f'Skipping raw_f1.{table_name} : No driver records found.')

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (driver_id, driver_name, driver_surname, driver_nationality, 
            driver_birthdate, driver_number, driver_short_name, team_id)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, drivers_record)
            self.conn.commit()
            print(f'Loaded {len(drivers_record)} records into PostgreSQL table raw_f1.{table_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{table_name}: {error}')
            if self.conn:
                self.conn.rollback()

    def teams(self,teams_url):

        try:
            data = self.fetch_api(teams_url)
            if not data: return

            table_name = 'teams'

            teams_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                teams_id VARCHAR(20), 
                team_name VARCHAR(50),
                team_nationality VARCHAR(20),
                first_appeareance INT,
                constructors_championships INT,
                drivers_championships INT 
            );"""

            self.cursor.execute(teams_table_schema)

            teams = data.get('teams')

            teams_record = []

            if teams is not None:
                for row in teams:
                    row = (
                        row.get('teamId'),
                        row.get('teamName'),
                        row.get('teamNationality'),
                        row.get('firstAppeareance'),
                        row.get('constructorsChampionships'),
                        row.get('driversChampionships')  
                    )

                    teams_record.append(row)

            else:
                print(f'Skipping raw_f1.{table_name} : No team records found.')

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (teams_id, team_name, team_nationality, first_appeareance, 
            constructors_championships, drivers_championships)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, teams_record)
            self.conn.commit()
            print(f'Loaded {len(teams_record)} records into PostgreSQL table raw_f1.{table_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{table_name} : {error}')
            if self.conn:
                self.conn.rollback()

    def season(self, season_url):

        try:
            data = self.fetch_api(season_url)
            if not data: return 

            table_name = 'season'

            season_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                championship_id VARCHAR(10), 
                championship_name VARCHAR(100),
                year INT
            );"""
    
            self.cursor.execute(season_table_schema)

            season = data.get('championships')

            season_record = []

            if season is not None:
                for row in season:
                    row = (
                        row.get('championshipId'),
                        row.get('championshipName'),
                        row.get('year')  
                    )

                    season_record.append(row)

            else:
                print(f'Skipping raw_f1.{table_name} : No season records found.')

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (championship_id, championship_name, year)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, season_record)
            self.conn.commit()
            print(f'Loaded {len(season_record)} records into PostgreSQL table raw_f1.{table_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{table_name}: {error}')
            if self.conn:
                self.conn.rollback()

    def free_practice(self, free_practice_url, session_name = 'free_practice'):

        try:
            data = self.fetch_api(free_practice_url)
            if not data: return

            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{session_name} (
                season INT,
                round INT, 
                fp_date DATE,
                fp_time TIME,
                race_id VARCHAR(50),
                race_name VARCHAR(100),
                circuit_id VARCHAR(50),
                circuit_name VARCHAR(50),
                country VARCHAR(50),
                city VARCHAR(50),
                circuit_length VARCHAR(30),
                lap_record VARCHAR(30),
                first_participation_year INT,
                corners INT,
                fastest_lap_driver_id VARCHAR(50),
                fastest_lap_team_id VARCHAR(50),
                fastest_lap_year INT,
                fp_id INT,
                time VARCHAR(20),
                driver_id VARCHAR(50),
                driver_name VARCHAR(50),
                driver_surname VARCHAR(50),
                driver_nationality VARCHAR(50),
                driver_number INT,
                driver_short_name VARCHAR(3),
                driver_birthday DATE,
                team_id VARCHAR(50),
                team_name VARCHAR(50),
                team_nationality VARCHAR(50),
                first_appearance INT,
                constructors_championships INT,
                drivers_championships INT
            );
            """)
            
            season = data.get('season')
            races = data.get('races')
            circuit = races.get('circuit')
            results = races.get('fp1Results') or races.get('fp2Results') or races.get('fp3Results')

            fp_record = [] 

            if results is not None: 
                for row in results:

                    driver_data = row.get('driver')
                    team_data = row.get('team')

                    records = (
                        season, races.get('round'), 
                        races.get('fp1Date') or races.get('fp2Date') or races.get('fp3Date'),
                        races.get('fp1Time') or races.get('fp2Time') or races.get('fp3Time'),
                        races.get('raceId'), races.get('raceName'), 
                        circuit.get('circuitId'), circuit.get('circuitName'), circuit.get('country'), circuit.get('city'), 
                        circuit.get('circuitLength'), circuit.get('lapRecord'), circuit.get('firstParticipationYear'), circuit.get('corners'), 
                        circuit.get('fastestLapDriverId'), circuit.get('fastestLapTeamId'), circuit.get('fastestLapYear'),
                        row.get('fp1Id') or row.get('fp2Id') or row.get('fp3Id'), row.get('time'),
                        driver_data.get('driverId'), driver_data.get('name'), driver_data.get('surname'), driver_data.get('nationality'),
                        driver_data.get('number'), driver_data.get('shortName'), driver_data.get('birthday'),
                        team_data.get('teamId'), team_data.get('teamName'), team_data.get('nationality'), team_data.get('firstAppareance'),
                        team_data.get('constructorsChampionships'), team_data.get('driversChampionships') 
                    )

                    fp_record.append(records)

            else:
                print(f'Skipping raw_f1.{session_name} : This weekend does not have Free Practice Results.')

            insert_query = f"""
            INSERT INTO raw_f1.{session_name} (season, round, fp_date, fp_time, 
            race_id, race_name, circuit_id, circuit_name, country, city, circuit_length, 
            lap_record, first_participation_year, corners, fastest_lap_driver_id, fastest_lap_team_id,
            fastest_lap_year, fp_id, time, driver_id, driver_name, driver_surname, driver_nationality,
            driver_number, driver_short_name, driver_birthday, team_id, team_name, team_nationality, 
            first_appearance, constructors_championships, drivers_championships)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, fp_record)
            self.conn.commit()
            print(f'Loaded {len(fp_record)} records into PostgreSQL table raw_f1.{session_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{session_name}: {error}')
            if self.conn:
                self.conn.rollback()

    def qualy_race(self, qualy_race_url):
    
        try:
            data = self.fetch_api(qualy_race_url)
            if not data: return 

            table_name = 'qualy_race'

            qualy_race_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                season INT,
                round INT,
                qualy_time TIME, 
                qualy_date DATE,
                race_id VARCHAR(30),
                race_name VARCHAR(100),
                circuit_id VARCHAR(20),
                circuit_name VARCHAR(20),
                country VARCHAR(20),
                city VARCHAR(20),
                circuit_length VARCHAR(10),
                lap_record VARCHAR(10),
                first_participation_year INT,
                corners INT,
                fastest_lap_driver_id VARCHAR(20),
                fastest_lap_team_id VARCHAR(20),
                fastest_lap_year INT,
                classification_id INT,
                driver_id VARCHAR(20),
                team_id VARCHAR(20),
                q1 VARCHAR(10),
                q2 VARCHAR(10),
                q3 VARCHAR(10),
                grid_position INT,
                driver_number INT,
                driver_short_name VARCHAR(3),
                driver_name VARCHAR(20),
                driver_surname VARCHAR(20),
                driver_nationality VARCHAR(20),
                driver_birthday DATE,
                team_name VARCHAR(30),
                team_nationality VARCHAR(20),
                first_appearance INT,
                constructors_championships INT,
                drivers_championships INT
            );"""
    
            self.cursor.execute(qualy_race_table_schema)

            season = data.get('season')
            races = data.get('races')
            circuit = races.get('circuit')
            results = races.get('qualyResults')

            qualy_race_record = []

            if qualy_race_record is not None:
                for row in results:

                    driver_data = row.get('driver')
                    team_data = row.get('team')

                    records = (
                        season, races.get('round'), races.get('qualyTime'), races.get('qualyDate'), races.get('raceId'), races.get('raceName'),
                        circuit.get('circuitId'), circuit.get('circuitName'), circuit.get('country'), circuit.get('city'), 
                        circuit.get('circuitLength'), circuit.get('lapRecord'), circuit.get('firstParticipationYear'), circuit.get('corners'),
                        circuit.get('fastestLapDriverId'), circuit.get('fastestLapTeamId'), circuit.get('fastestLapYear'), 
                        row.get('classificationId'), driver_data.get('driverId'), team_data.get('teamId'), row.get('q1'), row.get('q2'), row.get('q3'), 
                        row.get('gridPosition'), driver_data.get('number'), driver_data.get('shortName'),
                        driver_data.get('name'), driver_data.get('surname'), driver_data.get('nationality'), driver_data.get('birthday'), 
                        team_data.get('teamName'), team_data.get('nationality'), team_data.get('firstAppareance'),
                        team_data.get('constructorsChampionships'), team_data.get('driversChampionships') 
                    )

                    qualy_race_record.append(records)

            else:
                print(f'Skipping raw_f1.{table_name} : This weekend does not have Qualy Race Results.')        

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (season, round, qualy_time, qualy_date, 
            race_id, race_name, circuit_id, circuit_name, country, city, circuit_length, 
            lap_record, first_participation_year, corners, fastest_lap_driver_id, fastest_lap_team_id,
            fastest_lap_year, classification_id, driver_id, team_id, q1, q2, q3, grid_position, 
            driver_number, driver_short_name, driver_name, driver_surname, driver_nationality,
            driver_birthday, team_name, team_nationality, first_appearance, constructors_championships, drivers_championships)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, qualy_race_record)
            self.conn.commit()
            print(f'Loaded {len(qualy_race_record)} records into PostgreSQL table raw_f1.{table_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{table_name}: {error}')
            if self.conn:
                self.conn.rollback()

    def race(self, race_url):
        
        try:
            data = self.fetch_api(race_url)
            if not data: return

            table_name = 'race'

            race_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                season INT,
                round INT,
                race_date DATE,
                race_time TIME,
                race_id VARCHAR(30),
                race_name VARCHAR(100),
                circuit_id VARCHAR(20),
                circuit_name VARCHAR(20),
                country VARCHAR(20),
                city VARCHAR(20),
                circuit_length VARCHAR(10),
                lap_record VARCHAR(10),
                first_participation_year INT,
                corners INT,
                fastest_lap_driver_id VARCHAR(20),
                fastest_lap_team_id VARCHAR(20),
                fastest_lap_year INT,
                position VARCHAR(2),
                points INT,
                grid VARCHAR(50),
                total_time TIME,
                fast_lap TIME,
                retired VARCHAR(10),
                driver_id VARCHAR(20),
                driver_number INT,
                driver_short_name VARCHAR(3),
                driver_name VARCHAR(20),
                driver_surname VARCHAR(20),
                driver_nationality VARCHAR(20),
                driver_birthday DATE,
                team_id VARCHAR(20),
                team_name VARCHAR(30),
                team_nationality VARCHAR(20),
                first_appearance INT,
                constructors_championships INT,
                drivers_championships INT
            );"""
    
            self.cursor.execute(race_table_schema)

            season = data.get('season')
            races = data.get('races')
            circuit = races.get('circuit')           
            results = races.get('results')

            race_record = []

            if results is not None:
                for row in results:

                    driver_data = row.get('driver')
                    team_data = row.get('team')

                    records = (
                        season, races.get('round'), races.get('date'), races.get('time'), races.get('raceId'), races.get('raceName'),
                        circuit.get('circuitId'), circuit.get('circuitName'), circuit.get('country'), circuit.get('city'), 
                        circuit.get('circuitLength'), circuit.get('lapRecord'), circuit.get('firstParticipationYear'), circuit.get('corners'), 
                        circuit.get('fastestLapDriverId'), circuit.get('fastestLapTeamId'), circuit.get('fastestLapYear'), 
                        row.get('position'), row.get('points'), row.get('grid'), row.get('total_time'), row.get('fastLap'), row.get('retired'),
                        driver_data.get('driverId'), driver_data.get('number'), driver_data.get('shortName'),
                        driver_data.get('name'), driver_data.get('surname'), driver_data.get('nationality'), driver_data.get('birthday'), 
                        team_data.get('teamId'), team_data.get('teamName'), team_data.get('nationality'), team_data.get('firstAppareance'),
                        team_data.get('constructorsChampionships'), team_data.get('driversChampionships') 
                    )

                    race_record.append(records)

            else:
                print(f'Skipping raw_f1.{table_name} : This weekend does not have Race Results.')        

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (season, round, race_date, race_time, race_id, race_name, 
            circuit_id, circuit_name, country, city, circuit_length, 
            lap_record, first_participation_year, corners, fastest_lap_driver_id, fastest_lap_team_id, fastest_lap_year, 
            position, points, grid, total_time, fast_lap, retired, 
            driver_id, driver_number, driver_short_name, driver_name, driver_surname, driver_nationality, driver_birthday, 
            team_id, team_name, team_nationality, first_appearance, constructors_championships, drivers_championships)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, race_record)
            self.conn.commit()
            print(f'Loaded {len(race_record)} records into PostgreSQL table raw_f1.{table_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{table_name}: {error}')
            if self.conn:
                self.conn.rollback()    

    def sprint_qualy(self, sprint_qualy_url):
            
        try:
            data = self.fetch_api(sprint_qualy_url)
            if not data: return

            table_name = 'sprint_qualy'

            sprint_qualy_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                season INT,
                sprint_qualy_date DATE,
                sprint_qualy_time TIME,
                race_id VARCHAR(30),
                race_name VARCHAR(100),
                round INT,
                circuit_id VARCHAR(20),
                circuit_name VARCHAR(20),
                country VARCHAR(20),
                city VARCHAR(20),
                circuit_length VARCHAR(10),
                lap_record VARCHAR(10),
                first_participation_year INT,
                corners INT,
                fastest_lap_driver_id VARCHAR(20),
                fastest_lap_team_id VARCHAR(20),
                fastest_lap_year INT,
                sprint_qualy_id INT,
                sq1 TIME,
                sq2 TIME,
                sq3 TIME,
                grid_position INT,
                driver_id VARCHAR(20),
                driver_number INT,
                driver_short_name VARCHAR(3),
                driver_name VARCHAR(20),
                driver_surname VARCHAR(20),
                driver_nationality VARCHAR(20),
                driver_birthday DATE,
                team_id VARCHAR(20),
                team_name VARCHAR(30),
                team_nationality VARCHAR(20),
                first_appearance INT,
                constructors_championships INT,
                drivers_championships INT
            );"""
    
            self.cursor.execute(sprint_qualy_table_schema)
            
            season = data.get('season')
            races = data.get('races')
            circuit = races.get('circuit')
            sprintQualyResults = races.get('sprintQualyResults')

            sprint_qualy_record = []

            if sprintQualyResults is not None:

                for row in sprintQualyResults:

                    driver_data = row.get('driver')
                    team_data = row.get('team')

                    records = (
                        season, races.get('date'), races.get('time'), races.get('raceId'), races.get('raceName'), races.get('round'), 
                        circuit.get('circuitId'), circuit.get('circuitName'), circuit.get('country'), circuit.get('city'), 
                        circuit.get('circuitLength'), circuit.get('lapRecord'), circuit.get('firstParticipationYear'), circuit.get('corners'),
                        circuit.get('fastestLapDriverId'), circuit.get('fastestLapTeamId'), circuit.get('fastestLapYear'), 
                        row.get('sprintQualyId'), row.get('sq1'), row.get('sq2'), row.get('sq3'), row.get('gridPosition'),
                        driver_data.get('driverId'), driver_data.get('number'), driver_data.get('shortName'),
                        driver_data.get('name'), driver_data.get('surname'), driver_data.get('nationality'), driver_data.get('birthday'), 
                        team_data.get('teamId'), team_data.get('teamName'), team_data.get('nationality'), team_data.get('firstAppareance'),
                        team_data.get('constructorsChampionships'), team_data.get('driversChampionships') 
                    )

                    sprint_qualy_record.append(records)

            else:
                print(f'Skipping raw_f1.{table_name} : This weekend does not have Sprint Qualy Results.')

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (season, sprint_qualy_date, sprint_qualy_time, race_id, race_name, round,
            circuit_id, circuit_name, country, city, circuit_length, 
            lap_record, first_participation_year, corners, fastest_lap_driver_id, fastest_lap_team_id, fastest_lap_year, 
            sprint_qualy_id, sq1, sq2, sq3, grid_position, 
            driver_id, driver_number, driver_short_name, driver_name, driver_surname, driver_nationality, driver_birthday, 
            team_id, team_name, team_nationality, first_appearance, constructors_championships, drivers_championships)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, sprint_qualy_record)
            self.conn.commit()
            print(f'Loaded {len(sprint_qualy_record)} records into PostgreSQL table raw_f1.{table_name}.')
        
        except Exception as error:
            print(f'Error in raw_f1.{table_name}: {error}')
            if self.conn:
                self.conn.rollback()

    def sprint_race(self, sprint_race_url):
                
        try:
            data = self.fetch_api(sprint_race_url)
            if not data: return

            table_name = 'sprint_race'

            sprint_race_table_schema = f"""
            CREATE TABLE IF NOT EXISTS raw_f1.{table_name} (
                season INT,
                sprint_race_date DATE,
                sprint_race_start_time TIME,
                race_id VARCHAR(30),
                race_name VARCHAR(100),
                round INT,
                circuit_id VARCHAR(20),
                circuit_name VARCHAR(20),
                country VARCHAR(20),
                city VARCHAR(20),
                circuit_length VARCHAR(10),
                lap_record VARCHAR(10),
                first_participation_year INT,
                corners INT,
                fastest_lap_driver_id VARCHAR(20),
                fastest_lap_team_id VARCHAR(20),
                fastest_lap_year INT,
                sprint_race_id INT,
                position INT,
                points INT,
                grid INT,
                laps INT,
                time VARCHAR(10),
                retired VARCHAR(10),    
                driver_id VARCHAR(20),
                driver_number INT,
                driver_short_name VARCHAR(3),
                driver_name VARCHAR(20),
                driver_surname VARCHAR(20),
                driver_nationality VARCHAR(20),
                driver_birthday DATE,
                team_id VARCHAR(20),
                team_name VARCHAR(30),
                team_nationality VARCHAR(20),
                first_appearance INT,
                constructors_championships INT,
                drivers_championships INT
            );"""
    
            self.cursor.execute(sprint_race_table_schema)

            season = data.get('season')
            races = data.get('races')
            circuit = races.get('circuit')
            sprintRaceResults = races.get('sprintRaceResults')

            sprint_race_record = []

            if sprintRaceResults is not None:

                for row in sprintRaceResults:

                    driver_data = row.get('driver')
                    team_data = row.get('team')

                    records = (
                        season, races.get('date'), races.get('time'), 
                        races.get('raceId'), races.get('raceName'), races.get('round'), circuit.get('circuitId'), circuit.get('circuitName'), 
                        circuit.get('country'), circuit.get('city'), circuit.get('circuitLength'), circuit.get('lapRecord'),
                        circuit.get('firstParticipationYear'), circuit.get('corners'),  
                        circuit.get('fastestLapDriverId'), circuit.get('fastestLapTeamId'), circuit.get('fastestLapYear'), 
                        row.get('sprintRaceId'), row.get('position'), row.get('points'), row.get('grid'), row.get('laps'), row.get('time'), 
                        row.get('retired'), driver_data.get('driverId'), driver_data.get('number'), driver_data.get('shortName'),
                        driver_data.get('name'), driver_data.get('surname'), driver_data.get('nationality'), driver_data.get('birthday'), 
                        team_data.get('teamId'), team_data.get('teamName'), team_data.get('nationality'), team_data.get('firstAppareance'),
                        team_data.get('constructorsChampionships'), team_data.get('driversChampionships') 
                    )

                    sprint_race_record.append(records)

            else:
                print(f'Skipping raw_f1.{table_name} : This weekend does not have Sprint Race Results.')

            insert_query = f"""
            INSERT INTO raw_f1.{table_name} (season, sprint_race_date, sprint_race_start_time, race_id, race_name, round,
            circuit_id, circuit_name, country, city, circuit_length, 
            lap_record, first_participation_year, corners, fastest_lap_driver_id, fastest_lap_team_id, fastest_lap_year, 
            sprint_race_id, position, points, grid, laps, time, retired, 
            driver_id, driver_number, driver_short_name, driver_name, driver_surname, driver_nationality, driver_birthday, 
            team_id, team_name, team_nationality, first_appearance, constructors_championships, drivers_championships)
            VALUES %s;
            """

            execute_values(self.cursor, insert_query, sprint_race_record)
            self.conn.commit()
            print(f'Loaded {len(sprint_race_record)} records into PostgreSQL table raw_f1.{table_name}.')

        except Exception as error:
            print(f'Error in raw_f1.{table_name}: {error}')
            if self.conn:
                self.conn.rollback()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print('Database connection safely closed.')

if __name__ == '__main__': 

    pipeline = extraction_loading()

    try:
        pipeline.drivers('https://f1api.dev/api/current/drivers')
        pipeline.teams('https://f1api.dev/api/current/teams')
        pipeline.season('https://f1api.dev/api/seasons')
        pipeline.free_practice('https://f1api.dev/api/current/last/fp1', session_name = 'free_practice_1')
        pipeline.free_practice('https://f1api.dev/api/current/last/fp2', session_name = 'free_practice_2')
        pipeline.free_practice('https://f1api.dev/api/current/last/fp3', session_name = 'free_practice_3')
        pipeline.qualy_race('https://f1api.dev/api/current/last/qualy')
        pipeline.race('https://f1api.dev/api/current/last/race')
        pipeline.sprint_qualy('https://f1api.dev/api/current/last/sprint/qualy')
        pipeline.sprint_race('https://f1api.dev/api/current/last/sprint/race')

    finally:
        pipeline.close_connection()