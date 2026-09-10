"""
ORIS Data Scraper Module
Scrapes ranking and startovka data from ORIS website
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ORISScraper:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_ranking_data(self, ranking_url: str) -> pd.DataFrame:
        """
        Scrape ranking data from ORIS ranking page
        
        Args:
            ranking_url: URL to ORIS ranking page
            
        Returns:
            DataFrame with ranking data (name, coefficient, category)
        """
        try:
            logger.info(f"Fetching ranking data from {ranking_url}")
            response = self.session.get(ranking_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            data = []
            
            # Find ranking table
            tables = soup.find_all('table', {'class': 'ranking-table'})
            
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        try:
                            # Extract data: position, name, category, coefficient
                            position = cols[0].text.strip()
                            name = cols[1].text.strip()
                            category = cols[2].text.strip()
                            coefficient = float(cols[3].text.strip())
                            
                            data.append({
                                'position': position,
                                'name': name,
                                'category': category,
                                'coefficient': coefficient
                            })
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Error parsing row: {e}")
                            continue
            
            df = pd.DataFrame(data)
            logger.info(f"Successfully scraped {len(df)} ranking entries")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching ranking data: {e}")
            raise

    def get_startovka_data(self, startovka_url: str) -> pd.DataFrame:
        """
        Scrape startovka (entry list) data from ORIS
        
        Args:
            startovka_url: URL to ORIS startovka page
            
        Returns:
            DataFrame with entry data (name, category, start number)
        """
        try:
            logger.info(f"Fetching startovka data from {startovka_url}")
            response = self.session.get(startovka_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            data = []
            
            # Find startovka table
            tables = soup.find_all('table', {'class': 'startovka-table'})
            
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        try:
                            # Extract data: start number, name, category
                            start_num = cols[0].text.strip()
                            name = cols[1].text.strip()
                            category = cols[2].text.strip()
                            
                            data.append({
                                'start_number': start_num,
                                'name': name,
                                'category': category
                            })
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Error parsing row: {e}")
                            continue
            
            df = pd.DataFrame(data)
            logger.info(f"Successfully scraped {len(df)} startovka entries")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching startovka data: {e}")
            raise

    def close(self):
        """Close session"""
        self.session.close()
