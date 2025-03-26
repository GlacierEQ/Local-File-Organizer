#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check for root privileges
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: Please run as root (sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}Installing Bender Rodriguez System Service...${NC}"
echo

# Create Bender's home directory
echo "Creating Bender's home directory..."
mkdir -p ~/.bender/{logs,memory,models}

# Install system dependencies
echo "Installing system dependencies..."
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    apt-get update
    apt-get install -y python3-pip python3-venv libpython3-dev
elif [ -f /etc/redhat-release ]; then
    # RHEL/CentOS
    yum install -y python3-pip python3-devel
elif [ -f /etc/arch-release ]; then
    # Arch Linux
    pacman -Sy python-pip
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv /opt/bender
source /opt/bender/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements_ai.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install dependencies!${NC}"
    exit 1
fi

# Install the service
echo "Installing Bender service..."
python3 system_service/bender_service.py install
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install service!${NC}"
    exit 1
fi

# Start the service
echo "Starting Bender service..."
systemctl start bender
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to start service!${NC}"
    exit 1
fi

# Enable service on boot
systemctl enable bender

echo
echo -e "${GREEN}Bender Rodriguez has been successfully installed!${NC}"
echo "You can access his web interface at: http://localhost:5000"
echo
echo -e "${YELLOW}\"Bite my shiny metal ASCII!\"${NC}"
echo

# Add Bender to PATH
echo 'export PATH=$PATH:/opt/bender/bin' >> ~/.bashrc
source ~/.bashrc

# Create bender command
cat > /usr/local/bin/bender << 'EOF'
#!/bin/bash
case "$1" in
    start)
        systemctl start bender
        ;;
    stop)
        systemctl stop bender
        ;;
    restart)
        systemctl restart bender
        ;;
    status)
        systemctl status bender
        ;;
    logs)
        tail -f ~/.bender/logs/bender_service.log
        ;;
    web)
        xdg-open http://localhost:5000
        ;;
    memory)
        echo "Memory Status:"
        du -h ~/.bender/memory
        ;;
    models)
        echo "Installed Models:"
        ls -lh ~/.bender/models
        ;;
    update)
        systemctl stop bender
        source /opt/bender/bin/activate
        pip install -r requirements_ai.txt --upgrade
        systemctl start bender
        ;;
    *)
        echo "Usage: bender {start|stop|restart|status|logs|web|memory|models|update}"
        exit 1
        ;;
esac
exit 0
EOF

chmod +x /usr/local/bin/bender

# Create uninstall script
cat > /usr/local/bin/uninstall-bender << 'EOF'
#!/bin/bash
if [ "$EUID" -ne 0 ]; then 
    echo "Error: Please run as root (sudo)"
    exit 1
fi

systemctl stop bender
systemctl disable bender
rm -f /etc/systemd/system/bender.service
systemctl daemon-reload
rm -rf ~/.bender
rm -rf /opt/bender
rm -f /usr/local/bin/bender
echo "Bender has been uninstalled. He'll be back... with blackjack, and hookers!"
EOF

chmod +x /usr/local/bin/uninstall-bender

echo "Bender command installed. Try 'bender status' to check the service."
echo "To uninstall, run 'sudo uninstall-bender'"
