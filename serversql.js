import express from "express";
import axios from "axios";
import bodyParser from "body-parser";
import pg from "pg";
import env from "dotenv";

const app = express();
const port = 2000;
env.config();

const db = new pg.Client({
    user: process.env.USERNAME,
    host: process.env.HOST,
    database: process.env.DATABASE,
    password: process.env.DATA_PASSWORD,
    port: process.env.PORT
});
db.connect();

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(express.static("public"))
 
// get the home page 
app.get("/", async(req, res) => {
    try {
        const result = await db.query("SELECT * FROM posts");
        res.render("home.ejs", {poste: result.rows});
    } catch (error) {
        res
            .status(500) 
            .json({error: "Failed to get the Blog Web."})
    }
})

//get the features page
app.get("/features", (req, res) => {
    res.render("features.ejs")
})

// create a new post
app.post("/newpost", async(req, res) => {
    const da = new Date();
    try {
        const re = await db.query("INSERT INTO posts (author, subject, post, date) VALUES($1, $2, $3, $4)", [req.body.author, req.body.subject, req.body.post, da]);
        const result = await db.query("SELECT * FROM posts");
        res.render("home.ejs", {poste: result.rows, success_m: 'New post created successfully.'});
    } catch (error) {
        res.render("home.ejs", {poste: result.rows, error: "Failed to create post."});
    }
})

// edit a post
app.get("/edit/:id", async(req, res) => {
    const poId = parseInt(req.params.id);
    const result = await db.query("SELECT * FROM posts");
    try {
        const poF = await db.query("SELECT * FROM posts WHERE id = $1", [poId]);
        const poFound = poF.rows[0];
        res.render("edit.ejs", {pos: poFound})
    } catch (error) {
        res.render("home.ejs", {poste: result.rows, error: "Post not found."});
    }
})

app.post("/api/edit/:id", async(req, res) => {
    const da = new Date();
    const poId = parseInt(req.params.id);
    const poF = await db.query("SELECT * FROM posts WHERE id = $1", [poId]);
    const poFound = poF.rows[0];
    try {
        const re = await db.query("UPDATE posts SET author=$1, subject=$2, post=$3, date=$4 WHERE id=$5", [req.body.author, req.body.subject, req.body.post, da, req.params.id]);
        const result = await db.query("SELECT * FROM posts");
        res.redirect("/");
    } catch (error) {
        res.render("edit.ejs", {pos: poFound, error: "Failed to edit post."});
    }
})
 
// delete a post
app.get("/delete/:id", async(req, res) => {
    try {
        const re = await db.query("DELETE FROM posts WHERE id = $1", [req.params.id]);
        res.redirect("/");
    } catch (error) {
        res
            .status(500)
            .json({error: "Failed to delete post"});
    }
})

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
}) 