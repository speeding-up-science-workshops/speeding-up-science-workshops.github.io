---
title: Editing this Site 
date: 2019-05-10
authors:
  - N. Tessa Pierce (@bluegenes)
---
# Editing this Site

All the docs on this site are written in markdown (`.md` files) and built into an html site by `mkdocs`. If you want to edit
any of these documents, you can make changes to the corresponding markdown file (or add a new one), and then edit the `mkdocs`
configuration to make sure the file gets built into html. Read on for instructions!

## The first time you clone a repo with a mkdocs submodule:

If you want to edit the docs, you'll need to grab the `mkdocs-material-dib` submodule.

If you're cloning the repo for the first time:

```
git clone --recursive https://github.com/speeding-up-science-workshops/speeding-up-science
```
`recursive` will pull the submodule as well as the main git repo.


However, if you already have the repo, you'll want to pull down submodule like this:

```
git submodule update --init
```

## Installing the tools

We recommend conda for tool installation.

```
conda install  -c conda-forge mkdocs
conda install -c conda-forge ghp-import
```

## Where are the docs?

Each page on the website is a `markdown` document in the `docs` folder. These are organized by the 
navigation (`nav`) text in the `mkdocs.yml` file, which sits in the main directory. By looking at
the `mkdocs.yml` file, you can find the name of the markdown file you want to edit.

## Updating an Existing Page

If you're updating a file that already exists, start by making edits to the appropriate markdown file.
Then, you'll want to check that the markdown you wrote will be rendered properly. Assuming you've installed
mkdocs (above), you build the markdown into html like so:

```
mkdocs build
```

And then build a local site like so:
```
mkdocs serve
```

The site will now be rendered on your local computer (viewable in your web browser at the link that will come up on your screen with a successful `mkdocs serve`, like `http://127.0.0.1:8000/`)
and you can continue to make changes to your `md` file until it looks right. Stop the mkdocs serve by using `Ctrl-C`.

Note, if you're embedding images into your markdown, please name them appropriately (preferably including the name of your markdown file, e.g. `XY-workflow-img1.png`) and place them into the `docs/img` folder. This will keep our `docs` folder nice and clean.

When you're finished, commit your changes as you normally would, e.g.: 

```
git add <myfile.md>
git commit -m "some useful commit message"
```

And then build the site one last time and push to the `gh-pages` branch like so: 


**Note, you need to be in the main folder where the `mkdocs.yml` file is**
```
mkdocs build
ghp-import site -p
```

## Adding a New Page

If you want to add a new page, you'll need to add that file to the file navigation in the `mkdocs.yml` file. 
First go look at the `nav` sectino in `mkdocs.yml` while looking at the built site and figure out what section
you'd like to put your new page in. Then add your page to the `nav` like so:

```
- 'New-Title`: new-page.md
```
For more details, go [here](https://www.mkdocs.org/user-guide/configuration/).

Then, you'll need to go through the same steps as above, for *Updating an Existing Page*.

In short:

  - make changes to `md` file
  - `mkdocs build` to build html site
  - `mkdocs serve` to view page and navigation
  - repeat the above steps until satisfied
  - `git commit` (and `git push`) your changes 
  - `mkdocs build` and then `ghp-import site -p` to update the website

## Troubleshooting

If you see errors during `mkdocs build` or `mkdocs serve`, the likely culprit is improper formatting of the `nav` section in the `mkdocs.yml` file. Yaml is sensitive to spacing, quotes, etc! Check out the working pages and make your entry look like those! Any other issues? Submit an issue on github!

