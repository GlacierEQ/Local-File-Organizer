"""
Project enhancement script that uses name optimization, system analysis,
and program reorganization with 777 iterations for optimal results.
"""
import argparse
import logging
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

from core.name_optimizer import NameOptimizer
from core.system_analyzer import SystemAnalyzer
from core.program_reorganizer import ProgramReorganizer

def setup_logging(log_file: str = "project_enhancement.log"):
    """Set up logging configuration"""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def create_backup(project_dir: Path) -> Path:
    """Create a backup of the project"""
    backup_dir = project_dir.parent / f"{project_dir.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    import shutil
    shutil.copytree(project_dir, backup_dir)
    return backup_dir

def enhance_project(project_dir: str, target_dir: Optional[str] = None, 
                   skip_backup: bool = False):
    """
    Enhance a project by optimizing names, analyzing system health,
    and reorganizing program structure.
    
    Args:
        project_dir: Path to the project directory
        target_dir: Optional target directory for reorganized files
        skip_backup: Skip creating a backup if True
    """
    project_path = Path(project_dir).resolve()
    if not project_path.exists():
        raise ValueError(f"Project directory not found: {project_dir}")
    
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting project enhancement for: {project_dir}")
    
    # Create backup
    if not skip_backup:
        backup_path = create_backup(project_path)
        logger.info(f"Created backup at: {backup_path}")
    
    try:
        # Initialize components
        name_optimizer = NameOptimizer()
        system_analyzer = SystemAnalyzer(str(project_path))
        program_reorganizer = ProgramReorganizer(str(project_path))
        
        # Step 1: Analyze system health
        logger.info("Analyzing system health...")
        health_status = system_analyzer.check_system_health()
        logger.info(f"System health score: {health_status.score:.2f}%")
        
        if health_status.issues:
            logger.warning("System health issues found:")
            for issue in health_status.issues:
                logger.warning(f"- {issue}")
            
            logger.info("Recommendations:")
            for rec in health_status.recommendations:
                logger.info(f"- {rec}")
        
        # Step 2: Analyze dependencies
        logger.info("Analyzing dependencies...")
        dependencies = system_analyzer.analyze_dependencies()
        
        # Generate dependency visualization
        system_analyzer.visualize_dependencies("dependencies.html")
        logger.info("Generated dependency visualization: dependencies.html")
        
        # Step 3: Optimize system
        logger.info("Performing system optimizations...")
        optimization_results = system_analyzer.optimize_system()
        for result in optimization_results:
            logger.info(f"Optimization: {result}")
        
        # Step 4: Reorganize programs
        logger.info("Reorganizing program structure...")
        programs = program_reorganizer.reorganize(target_dir)
        
        # Generate reports
        reports_dir = project_path / "enhancement_reports"
        reports_dir.mkdir(exist_ok=True)
        
        # System analysis report
        system_report = system_analyzer.generate_report()
        with open(reports_dir / "system_analysis.json", 'w') as f:
            json.dump(system_report, f, indent=2)
        
        # Program organization report
        org_report = program_reorganizer.generate_report(programs)
        with open(reports_dir / "reorganization_report.txt", 'w') as f:
            f.write(org_report)
        
        logger.info(f"Enhancement reports generated in: {reports_dir}")
        
        # Final summary
        logger.info("\nProject Enhancement Summary:")
        logger.info("-" * 30)
        logger.info(f"System Health Score: {health_status.score:.2f}%")
        logger.info(f"Programs Identified: {len(programs)}")
        logger.info(f"Optimizations Performed: {len(optimization_results)}")
        logger.info(f"Reports Location: {reports_dir}")
        
        if not skip_backup:
            logger.info(f"Backup Location: {backup_path}")
        
        logger.info("\nEnhancement completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during enhancement: {str(e)}")
        if not skip_backup:
            logger.info(f"Project backup available at: {backup_path}")
        raise

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Enhance project structure and organization"
    )
    parser.add_argument(
        "project_dir",
        help="Path to the project directory"
    )
    parser.add_argument(
        "--target-dir",
        help="Optional target directory for reorganized files"
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="Skip creating a backup of the project"
    )
    
    args = parser.parse_args()
    
    try:
        enhance_project(
            args.project_dir,
            args.target_dir,
            args.skip_backup
        )
    except Exception as e:
        logging.error(f"Enhancement failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
