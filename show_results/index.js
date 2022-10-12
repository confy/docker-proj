// Make a login route that keeps a session
// and redirects to the results page
// if the user is logged in

import express, { json, urlencoded } from 'express';
import session from 'express-session';
import { join } from 'path';
import fetch from 'node-fetch';
import path from 'node:path'
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true
}));

app.use(json());
app.use(urlencoded({ extended: true }));
app.use(express.static(join(__dirname, 'static')));

// http://localhost:3000/
app.get('/', (req, res) => {
    if (req.session.loggedin) {
        // Render results
        res.redirect('/results');
    } else {
        // Render login
        res.sendFile(join(__dirname + '/static/login.html'));
    }
});

// Authenticates the user
// http://localhost:3000/auth
app.post('/auth', async (req, res) => {
    // Get input
    const username = req.body.username;
    const password = req.body.password;

    // Make sure they're not empty
    if (username && password) {
        // Check if the user exists
        const url = `http://localhost/`;
        console.log(url)
        const raw_response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        
        if (raw_response.status == 200) {
            // Set session
            req.session.loggedin = true;
            req.session.username = username;
            // Redirect to results
            res.redirect('/results');
        } else {
            // Render login
            res.sendFile(join(__dirname + '/static/login.html'));
        }

    }
});

app.get('/results', (req, res) => {
    if (req.session.loggedin) {
        // Render results
        res.send("HAHAHAHAHAHAHAHA")
    } else {
        // Render login
        res.sendFile(join(__dirname + '/static/login.html'));
    }
});

app.listen(80, () => {
    console.log('Server started on port 3000');
});