"""
Ranking Coefficient Agent
Main orchestration module that coordinates all components
"""

import logging
from typing import Dict, Optional
from config import (
    RANKING_URL, STARTOVKA_URL, TARGET_CATEGORIES,
    CATEGORY_NAMES, OUTPUT_DIR, PDF_FILENAME
)
from scraper import ORISScraper
from analyzer import RankingAnalyzer
from report_generator import PDFReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RankingCoefficientAgent:
    """
    Main agent for ranking coefficient analysis
    Orchestrates data collection, analysis, and reporting
    """
    
    def __init__(
        self,
        ranking_url: str = RANKING_URL,
        startovka_url: str = STARTOVKA_URL,
        target_categories: list = TARGET_CATEGORIES,
        output_dir: str = OUTPUT_DIR,
        pdf_filename: str = PDF_FILENAME
    ):
        """
        Initialize the agent
        
        Args:
            ranking_url: URL to ORIS ranking page
            startovka_url: URL to ORIS startovka page
            target_categories: List of categories to analyze
            output_dir: Output directory for reports
            pdf_filename: Output PDF filename
        """
        self.ranking_url = ranking_url
        self.startovka_url = startovka_url
        self.target_categories = target_categories
        self.output_dir = output_dir
        self.pdf_filename = pdf_filename
        
        self.scraper = None
        self.analyzer = RankingAnalyzer()
        self.report_generator = PDFReportGenerator(output_dir)
        
        logger.info("Ranking Coefficient Agent initialized")

    def run(self) -> Dict:
        """
        Run the complete analysis workflow
        
        Returns:
            Dict with analysis results and report path
        """
        try:
            logger.info("=" * 60)
            logger.info("Starting Ranking Coefficient Analysis")
            logger.info("=" * 60)
            
            # Step 1: Scrape data
            logger.info("\n[STEP 1] Fetching data from ORIS...")
            ranking_df = self._fetch_ranking_data()
            
            if ranking_df is None or len(ranking_df) == 0:
                logger.error("Failed to fetch ranking data")
                return {
                    'success': False,
                    'error': 'No ranking data available',
                    'report_path': None
                }
            
            # Step 2: Analyze data
            logger.info("\n[STEP 2] Analyzing ranking coefficients...")
            results = self._analyze_data(ranking_df)
            
            # Step 3: Generate report
            logger.info("\n[STEP 3] Generating PDF report...")
            report_path = self._generate_report(results)
            
            logger.info("\n" + "=" * 60)
            logger.info("Analysis completed successfully!")
            logger.info(f"Report saved to: {report_path}")
            logger.info("=" * 60)
            
            return {
                'success': True,
                'results': results,
                'report_path': report_path,
                'data_rows': len(ranking_df)
            }
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'report_path': None
            }
        
        finally:
            self._cleanup()

    def _fetch_ranking_data(self):
        """
        Fetch ranking data from ORIS
        
        Returns:
            DataFrame with ranking data or None if failed
        """
        try:
            self.scraper = ORISScraper()
            logger.info(f"Fetching from: {self.ranking_url}")
            ranking_df = self.scraper.get_ranking_data(self.ranking_url)
            
            logger.info(f"Successfully fetched {len(ranking_df)} records")
            logger.info("\nAvailable categories in data:")
            for cat in ranking_df['category'].unique():
                count = len(ranking_df[ranking_df['category'] == cat])
                logger.info(f"  - {cat.strip()}: {count} entries")
            
            return ranking_df
            
        except Exception as e:
            logger.error(f"Error fetching ranking data: {e}")
            return None

    def _analyze_data(self, ranking_df) -> Dict:
        """
        Analyze ranking data
        
        Args:
            ranking_df: DataFrame with ranking data
            
        Returns:
            Dict with analysis results
        """
        try:
            logger.info(f"Analyzing {len(self.target_categories)} categories: {self.target_categories}")
            results = self.analyzer.analyze_all_categories(
                ranking_df,
                self.target_categories
            )
            
            logger.info("\nAnalysis Results:")
            for category, data in results.items():
                status = data.get('status', 'UNKNOWN')
                coefficient = data.get('coefficient', 0)
                logger.info(f"  {category}: {coefficient:.4f} (Status: {status})")
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing data: {e}")
            return {}

    def _generate_report(self, results: Dict) -> Optional[str]:
        """
        Generate PDF report
        
        Args:
            results: Analysis results
            
        Returns:
            Path to generated PDF or None if failed
        """
        try:
            report_path = self.report_generator.generate_report(
                results,
                CATEGORY_NAMES,
                self.pdf_filename
            )
            logger.info(f"PDF Report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None

    def _cleanup(self):
        """Clean up resources"""
        if self.scraper:
            self.scraper.close()
            logger.info("Scraper session closed")


def main():
    """Main entry point"""
    agent = RankingCoefficientAgent()
    result = agent.run()
    
    print("\n" + "=" * 60)
    print("AGENT EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Success: {result.get('success', False)}")
    
    if result.get('success'):
        print(f"Data rows processed: {result.get('data_rows', 0)}")
        print(f"Report location: {result.get('report_path', 'N/A')}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
