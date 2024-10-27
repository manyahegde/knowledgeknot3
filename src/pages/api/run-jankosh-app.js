// pages/api/run-jnankosh-app.js
import { exec } from 'child_process';

export default function handler(req, res) {
  console.log("Starting app.py execution...");

  // Adjust the path to where your Python app.py is located
  exec('python ../../JnanKosh-main/app.py', { timeout: 10000 }, (error, stdout, stderr) => {
    console.log("Execution completed.");

    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).json({ message: 'Error running app.py', error: error.message });
    }
    
    if (stderr) {
      console.error(`Stderr: ${stderr}`);
      return res.status(500).json({ message: 'Error running app.py', stderr });
    }

    console.log(`Stdout: ${stdout}`);
    res.status(200).json({ message: 'app.py executed successfully', output: stdout });
  });
}
