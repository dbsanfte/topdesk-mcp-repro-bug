const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// Add middleware to parse JSON body
app.use(express.json());

// Load routes configuration
let routes = [];
const configPath = process.env.ROUTES_CONFIG || '/app/config/routes.json';

try {
  const routesData = fs.readFileSync(configPath, 'utf8');
  routes = JSON.parse(routesData);
  console.log('Loaded routes configuration:', routes);
} catch (error) {
  console.error('Error loading routes configuration:', error);
  process.exit(1);
}

// Set up routes based on configuration
routes.forEach(route => {
  const routePath = route.path;
  const method = route.method?.toLowerCase() || 'get';
  const responseFile = route.response;
  
  if (!routePath || !responseFile) {
    console.error('Invalid route configuration:', route);
    return;
  }
  
  if (!app[method]) {
    console.error(`Unsupported HTTP method '${method}' for path '${routePath}'`);
    return;
  }
  
  app[method](routePath, (req, res) => {
    const filePath = path.join('/app/responses', responseFile);
    
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        console.error(`Error reading ${filePath}:`, err);
        return res.status(500).json({ error: `Could not load ${responseFile}` });
      }
      
      try {
        const jsonData = JSON.parse(data);
        res.json(jsonData);
      } catch (parseErr) {
        console.error(`Error parsing ${filePath}:`, parseErr);
        res.status(500).json({ error: `Invalid JSON in ${responseFile}` });
      }
    });
  });
  
  console.log(`Configured ${method.toUpperCase()} endpoint: ${routePath} -> ${responseFile}`);
});

// Add a health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});