import random
from django import forms
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import Markdown

from . import util


class SearchForm(forms.Form):
    '''
    A Form class for the search box in the sidebar to
    search for an encyclopedia entry.
    '''
    title = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search'
        }))


class NewPageForm(forms.Form):
    '''
    A Form class for creating a new encyclopedia entry.
    '''
    title = forms.CharField(
        required=True,
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the title of the page',
            'style': 'width: 50em;'
        }))
    content = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter the Markdown content of the page',
            'style': 'height: 10em; width: 50em;'
        }))


class EditPageForm(forms.Form):
    '''
    A Form class for editing an encyclopedia entry.
    '''
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter the Markdown content for the page',
            'style': 'height: 10em; width: 50em;'
        }))


def index(request):
    '''
    It lists the names of all pages in the encyclopedia (all entries).
    '''
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries(),
        'search': SearchForm()
    })


def entry_page(request, title):
    '''
    It renders a page that displays the contents of a requested
    encyclopedia entry if the entry exists.

    Format: /wiki/TITLE, where TITLE is the title of an encyclopedia entry

    If a requested entry does not exist, the user is presented with
    an error page indicating that the requested page was not found.
    '''
    entry_markdown = util.get_entry(title)

    if entry_markdown is not None:
        # a requested entry does exist
        entry_html = Markdown().convert(entry_markdown)
        return render(request, 'encyclopedia/entry_page.html', {
            'title': title,
            'entry': entry_html,
            'search': SearchForm()
        })
    else:
        # a requested entry does not exist
        messages.error(
            request,
            f'An encyclopedia entry with the title "{title}" does not exist.'
        )
        return render(request, 'encyclopedia/not_found.html', {
            'title': title,
            'search': SearchForm()
        })


def search(request):
    '''
    It allows the user to search for an encyclopedia entry.

    If the query matches the name of an encyclopedia entry,
    the user is redirected to that entry’s page.

    If the query does not match the name of an encyclopedia entry,
    the user is taken to a search results page that displays
    a list of all encyclopedia entries that have the query as a substring.
    '''
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            entry_markdown = util.get_entry(title)

            if entry_markdown is not None:
                # the query matches the name of an encyclopedia entry
                return redirect(reverse('entry_page', args=[title]))
            else:
                # the query does not match the name of an encyclopedia entry
                related_results = util.get_related_results(title)
                return render(request, 'encyclopedia/search.html', {
                    'title': title,
                    'related_results': related_results,
                    'search': SearchForm()
                })
    return redirect(reverse('index'))


def new_page(request):
    '''
    It allows the user to create a new encyclopedia entry.

    If an encyclopedia entry with the provided title already exists,
    the user is presented with an error message.
    '''
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html', {
            'form': NewPageForm(),
            'search': SearchForm()
        })

    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')

            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                messages.error(
                    request,
                    f'An encyclopedia entry with the title "{title}" already exists.'
                )
                return render(request, 'encyclopedia/new_page.html', {
                    'form': form,
                    'search': SearchForm()
                })
            else:
                util.save_entry(title, content)
                messages.success(
                    request,
                    f'The new encyclopedia entry "{title}" created successfully.'
                )
                return redirect(reverse('entry_page', args=[title]))
        else:
            messages.error(
                request,
                'There were some problems with your entry. Please try again.'
            )
            return render(request, 'encyclopedia/new_page.html', {
                'form': form,
                'search': SearchForm()
            })


def edit_page(request, title):
    '''
    It allows the user to edit an encyclopedia entry.
    '''
    if request.method == 'GET':
        entry = util.get_entry(title)

        if entry is None:
            messages.error(
                request,
                'An encyclopedia entry with the provided title does not exist.'
            )
            return render(request, 'encyclopedia/new_page.html', {
                'form': NewPageForm(),
                'search': SearchForm()
            })
        else:
            return render(request, 'encyclopedia/edit_page.html', {
                'title': title,
                'form': EditPageForm(initial={'content': entry}),
                'search': SearchForm()
            })

    if request.method == 'POST':
        form = EditPageForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            messages.success(
                request,
                f'The encyclopedia entry "{title}" updated successfully.'
            )
            return redirect(reverse('entry_page', args=[title]))
        else:
            messages.error(
                request,
                'There were some problems with your entry. Please try again.'
            )
            return render(request, 'encyclopedia/edit_page.html', {
                'title': title,
                'form': form,
                'search': SearchForm()
            })


def random_page(request):
    '''
    It takes the user to a random encyclopedia entry.
    '''
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect(reverse('entry_page', args=[entry]))
