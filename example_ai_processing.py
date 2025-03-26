import os
from legal_ai_processor import LegalAIProcessor

def main():
    # Initialize the AI processor
    processor = LegalAIProcessor()
    
    # Define input and output directories
    input_dir = "documents"  # Directory containing your legal documents
    output_dir = "consolidated_documents"  # Directory where consolidated files will be saved
    
    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Process all documents in the input directory
        print(f"Processing documents from: {input_dir}")
        processor.process_directory(input_dir, output_dir)
        
        print("\nProcessing complete!")
        print(f"Consolidated documents have been saved to: {output_dir}")
        print("\nGenerated files:")
        for doc_type in ['case_law', 'docket_entries', 'pleadings', 'exhibits']:
            file_path = os.path.join(output_dir, f"{doc_type}_consolidated.docx")
            if os.path.exists(file_path):
                print(f"- {file_path}")
                
    except Exception as e:
        print(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    main()
