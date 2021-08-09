# Wiki

A Wikipedia-like online encyclopedia.

## Background

Wikipedia is a free online encyclopedia that consists of a number of encyclopedia entries on various topics.

Each encyclopedia entry can be viewed by visiting that entry’s page. Visiting https://en.wikipedia.org/wiki/HTML, for example, shows the Wikipedia entry for HTML. The name of the requested page (HTML) is specified in the route `/wiki/HTML`. The content of the page is just HTML that a browser renders.

In practice, it would start to get tedious if every page on Wikipedia had to be written in HTML. So instead, it can be helpful to store encyclopedia entries using a lighter-weight human-friendly markup language. Wikipedia uses a markup language called `Wikitext`, but for this project, encyclopedia entries are stored using a markup language called [Markdown](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

By having one Markdown file represent each encyclopedia entry, we can make our entries more human-friendly to write and edit. When a user views our encyclopedia entry, the Markdown is converted into HTML before displaying it to the user.

## Specification

* **Entry Page**: Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, renders a page that displays the contents of that encyclopedia entry.
    * The view gets the content of the encyclopedia entry by calling the appropriate `util` function.
    * If an entry is requested that does not exist, the user is presented with an error page indicating that their requested page was not found.
    * If the entry does exist, the user is presented with a page that displays the content of the entry. The title of the page includes the name of the entry.
* **Index Page**: The`index.html` lists the names of all pages in the encyclopedia. Furthermore, the user can click on any entry name to be taken directly to that entry page.
* **Search**: The user can type a query into the search box in the sidebar to search for an encyclopedia entry.
    * If the query matches the name of an encyclopedia entry, the user is redirected to that entry’s page.
    * If the query does not match the name of an encyclopedia entry, the user is instead taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. So, for example, if the search query were `ytho`, then `Python` would appear in the search results.
    * Clicking on any of the entry names on the search results page takes the user to that entry’s page.
* **New Page**: Clicking “Create New Page” in the sidebar takes the user to a page where they can create a new encyclopedia entry.
    * Users can enter a title for the page and, in a textarea, can enter the Markdown content for the page.
    * Users can click a button to save their new page.
    * When the page is saved, if an encyclopedia entry already exists with the provided title, the user is presented with an error message.
    * Otherwise, the encyclopedia entry is saved to disk, and the user is taken to the new entry’s page.
* **Edit Page**: On each entry page, the user can click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
    * The textarea is pre-populated with the existing Markdown content of the page (i.e., the existing content is the initial value of the textarea).
    * The user can click a button to save the changes made to the entry.
    * Once the entry is saved, the user is redirected back to that entry’s page.
* **Random Page**: Clicking “Random Page” in the sidebar takes the user to a random encyclopedia entry.
* **Markdown to HTML Conversion**: On each entry’s page, any Markdown content in the entry file is converted to HTML before being displayed to the user.
