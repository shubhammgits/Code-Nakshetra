const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const cors = require('cors');
const path = require('path');

dotenv.config();
const app = express();

// ✅ Middleware
app.use(express.json());
app.use(cors());  // ✅ Allow all origins for local development

// ✅ MongoDB Connection
mongoose.connect('mongodb://127.0.0.1:27017/mydatabase', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log("✅ MongoDB Connected!"))
  .catch(err => console.log("❌ MongoDB Connection Error:", err));

// ✅ Test Route
app.get("/", (req, res) => {
    res.json({ message: "✅ Server is working!" });
});

// ✅ Authentication Routes
app.use('/auth', require('./routes/auth'));

// ✅ Signup Route (Ensuring JSON Response)
app.post('/auth/signup', async (req, res) => {
    try {
        const { username, email, password } = req.body;

        if (!username || !email || !password) {
            return res.status(400).json({ error: "❌ All fields are required!" });
        }

        // TODO: Add user creation logic here (e.g., saving user to MongoDB)

        res.json({ message: "✅ Signup successful!" });
    } catch (error) {
        res.status(500).json({ error: "❌ Internal Server Error" });
    }
});

// ✅ Login Route
app.post('/auth/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ error: "❌ Email and password are required!" });
        }

        // TODO: Add authentication logic here (e.g., checking user in MongoDB)

        res.json({ message: "✅ Login successful!" });
    } catch (error) {
        res.status(500).json({ error: "❌ Internal Server Error" });
    }
});

// ✅ Start HTTP Server (Local Development)
const PORT = 8000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});

require('dotenv').config();
