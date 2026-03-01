# Vercel Deployment Setup Script

echo "================================"
echo "  Vercel Deployment Setup"
echo "================================"
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel
echo ""
echo "Logging in to Vercel..."
vercel login

# Initialize project
echo ""
echo "Initializing Vercel project..."
vercel link

# Add environment variables
echo ""
echo "Setting up environment variables..."
echo "You'll be prompted to add DATABASE_URL"
vercel env add DATABASE_URL

# Deploy
echo ""
echo "Deploying to Vercel..."
vercel --prod

echo ""
echo "================================"
echo "  Deployment Complete!"
echo "================================"
echo ""
echo "Your app is now live on Vercel!"
echo "Open Vercel dashboard: vercel open"
