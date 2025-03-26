import threading
import time
import logging
import blackbox_ai
import document_sorter
from ai.central_ai import CentralIntelligenceAI
from ai.forensic_ai import ForensicAI
from ai.continuous_learning_ai import ContinuousLearningAI
from typing import List, Dict

logging.basicConfig(filename='auto_evolve_project.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def auto_evolve_blackbox(interval: int = 60) -> None:
    """
    Periodically evolve the blackbox AI.
    
    Args:
        interval (int): Time interval between evolutions in seconds.
    """
    while True:
        try:
            blackbox_ai.evolve_blackbox()
            logging.info("Blackbox AI evolved successfully.")
        except Exception as e:
            logging.error(f"Error evolving Blackbox AI: {e}")
        time.sleep(interval)

def auto_sort_documents(interval: int = 300) -> None:
    """
    Periodically sort documents using the document sorter.
    
    Args:
        interval (int): Time interval between sorting in seconds.
    """
    while True:
        try:
            document_sorter.sort_documents()
            logging.info("Documents sorted successfully.")
        except Exception as e:
            logging.error(f"Error sorting documents: {e}")
        time.sleep(interval)

def auto_forensic_audit(interval: int = 180) -> None:
    """
    Periodically perform forensic audits using the Forensic AI.
    
    Args:
        interval (int): Time interval between audits in seconds.
    """
    central = CentralIntelligenceAI()
    fa = ForensicAI(central)
    while True:
        try:
            fa.maintain_audit_trail()
            logging.info("Forensic audit trail maintained successfully.")
        except Exception as e:
            logging.error(f"Error maintaining forensic audit trail: {e}")
        time.sleep(interval)

def auto_update_continuous_learning(interval: int = 240) -> None:
    """
    Periodically update the continuous learning model.
    
    Args:
        interval (int): Time interval between updates in seconds.
    """
    central = CentralIntelligenceAI()
    cla = ContinuousLearningAI(central)
    data = [[0.0] * 10]
    labels = [0]
    while True:
        try:
            cla.update_model(data, labels)
            logging.info("Continuous learning model updated successfully.")
        except Exception as e:
            logging.error(f"Error updating continuous learning model: {e}")
        time.sleep(interval)

def adaptive_evolve(interval: int = 120) -> None:
    """
    Monitor module statuses and trigger remedial evolution if needed.
    
    Args:
        interval (int): Time interval between status checks in seconds.
    """
    central = CentralIntelligenceAI()
    while True:
        try:
            status: Dict[str, str] = central.get_status()
            inactive: List[str] = [mod for mod, state in status.items() if state != "Active"]
            if inactive:
                logging.warning(f"Modules inactive: {inactive}. Triggering remedial evolution.")
                blackbox_ai.evolve_blackbox()  # Use as a generic evolution function
            else:
                logging.info("All modules active.")
        except Exception as e:
            logging.error(f"Error in adaptive evolution: {e}")
        time.sleep(interval)

def hybrid_evolve(interval: int = 180) -> None:
    """
    Integrated evolution: combine multiple evolution actions into one cycle.
    
    Args:
        interval (int): Time interval between evolution cycles in seconds.
    """
    central = CentralIntelligenceAI()
    while True:
        try:
            logging.info("Hybrid evolution: starting integrated evolution cycle.")
            # Trigger evolution in Blackbox AI
            blackbox_ai.evolve_blackbox()
            # Optionally, you can add more evolution steps here such as additional diagnostics based on Central AI status.
            status: Dict[str, str] = central.get_status()
            if any(state != "Active" for state in status.values()):
                logging.warning("Hybrid evolution: Some modules report inactive states. Remedial actions triggered.")
                # For demonstration, triggering Blackbox evolution as a remedial action.
                blackbox_ai.evolve_blackbox()
            else:
                logging.info("Hybrid evolution: System modules operational.")
            logging.info("Hybrid evolution cycle complete.")
        except Exception as e:
            logging.error(f"Error in hybrid evolution: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    threads = [
        threading.Thread(target=auto_evolve_blackbox, args=(60,), daemon=True),
        threading.Thread(target=auto_sort_documents, args=(300,), daemon=True),
        threading.Thread(target=auto_forensic_audit, args=(180,), daemon=True),
        threading.Thread(target=auto_update_continuous_learning, args=(240,), daemon=True),
        threading.Thread(target=adaptive_evolve, args=(120,), daemon=True),
        threading.Thread(target=hybrid_evolve, args=(180,), daemon=True),
    ]
    for t in threads:
        t.start()
    print("Automated evolution running across all project areas with adaptive and hybrid evolution. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Automated evolution stopped.")
