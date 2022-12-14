// Make a login route that keeps a session
// and redirects to the results page
// if the user is logged in

import express, { json, urlencoded } from 'express';
import session from 'express-session';
import {default as connectMongoDBSession} from 'connect-mongodb-session'
const MongoDBStore = connectMongoDBSession(session)
import { join } from 'path';
import fetch from 'node-fetch';
import path from 'node:path'
import { fileURLToPath } from 'url';
import { MongoClient } from 'mongodb';
import ejsLayouts from 'express-ejs-layouts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

const MONGO_USER = process.env.MONGO_USER;
const MONGO_PASSWORD = process.env.MONGO_PASSWORD;
const MONGO_HOST = process.env.MONGO_HOST;
const MONGO_PORT = process.env.MONGO_PORT;
const uri_mongo = `mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/?retryWrites=true&w=majority`;
const client = new MongoClient(uri_mongo);

var store = new MongoDBStore({
    uri: uri_mongo,
    collection: 'mySessions'
});

store.on('error', function(error) {
console.log(error);
});

app.use(session({
    store: store,
    secret: 'secret',
    cookie: {
        maxAge: 1000 * 60 * 60 * 24 * 7 // 1 week
      },
    resave: true,
    saveUninitialized: true
}));

app.use(json());
app.use(urlencoded({ extended: true }));
app.use(express.static(join(__dirname, 'static')));

app.set("view engine", "ejs");
app.use(ejsLayouts);

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
        const url = `http://${process.env.HOSTNAME}`;
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

app.get('/results', async (req, res) => {
    if (req.session.loggedin) {
        // Get results from MongoDB
        await client.connect()
        const mongo_db = client.db(process.env.MONGO_DATABASE);
        const collection = mongo_db.collection('stats')
        const findResult = await collection
            .find().toArray();
        res.render('results', {data: findResult});
    } else {
        // Render login
        res.sendFile(join(__dirname + '/static/login.html'));
    }
});

app.listen(80, () => {
    console.log('Server started on port 3000');
});