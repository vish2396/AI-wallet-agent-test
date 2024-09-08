export default async function handler(req: any, res: any) {
    if (req.method === 'POST') {
      const { message } = JSON.parse(req.body);
  
      // Forward the request to your Python Flask API
      const response = await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
  
      const data = await response.json();
      res.status(200).json(data);
    } else {
      res.status(405).json({ message: 'Only POST requests allowed' });
    }
  }
  