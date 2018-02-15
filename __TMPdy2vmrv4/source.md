---
title: "EDLM: proposal"
author:
 - 132nd-etcher
author-meta: 132nd-etcher
applies:
 - 132^nd^ Virtual Wing
audience: CMD
status: in writing
title_pictures: [logo617th.png,logo696th.png,logo176th.png,logo23rd.png,logo259th.png,logo765th.png]
subtitle: Documentation overhaul
type: Enhancement Proposal
version: 0
published_date: unpublished
responsible: etcher
summary_of_changes:
 - nil
---


![Documentation](https://i.imgur.com/DNB0lco.png)

# Enhancement Proposal

## Abstract

This document contains an enhancement proposal submitted to CMD for review.

The proposal is about documentation in the 132^nd^ Virtual Wing. I would like to explore 
possible ways to make it better, easier to produce and easier to maintain.

## Rationale

I was working a while back on the 696^th^ TURNSKINS TRP (which produced no useful end-result), 
and was taken aback by many of Microsoft Word pitfalls. Why does it decide to 
auto-format so many things on my behalf ? And why can't it keep it consistent? 
Reznik and I were editing with different locale settings (fr_BE and da_DK), which 
added even more fun to the mix: different paper size, different quote characters, 
and so on ...

I've also been offered the chance to review the new 176^th^ EYES OF THE NORTH SOP before it officially 
came out, and the whole review process, using a proxy Google Docs temporary document 
seemed archaic and painful to me. This extra step adds a lot of undesirable overhead 
to the process.

Last example: as a side-project, I'm maintaining a knee board document written with 
Microsoft Excel, and that takes the pain to a whole new level.

I would like to propose a solution to get rid of those issues, and implement a better 
work flow for everyone. This document is published for review in order to assess how 
interested/willing people are interested to give it a try.

## Objective

What I'm trying to achieve:

* Increase quality and consistency of the (already 
astonishingly excellent) documentation;
* Allow for easier collaboration and review;
* Maintain an easy work flow for everyone.

What I'm trying to get rid of:

* Variations in style or formatting;
* Older documents not updated to the latest layout/formatting;
* Older documents containing outdated information;
* Dead links in documents that haven't been updated for a while;
* Passing documents around during review/editing process.

## Examples

You can find a few documents that have been generated with the method I'm proposing 
here: [http://132virtualwing.org/files/docs/PDF/](http://132virtualwing.org/files/docs/PDF/).

And this is the Github repository in which all those documents live: 
[https://github.com/132nd-etcher/docs](https://github.com/132nd-etcher/docs).

*Note*: this very document is part of that library =)

## Getting there

This section conceptually describes how to achieve the goals outlined above.

### Decoupling the content from the format

Writing a document with Microsoft Office Word implies formatting it as well. 
Despite the use of a template, guaranteeing a consistent format across a library 
of dozens of documents, written by many authors, sometimes even multiple authors 
for the same document, is almost impossible.

Due to the inherent complexity of Microsoft Word Office, as well as the debatable 
pertinence of some choices it sometimes seems to automatically make for us, some 
subtle format changes are bound to sneak unnoticed within the documents over time.

My first goal is to get rid of this ambiguity, and have one and only one way to 
express a given construct (a paragraph, a heading, a list, a table, ...).

This would also have the beneficial side effect of freeing editors from worrying 
about formatting their content while they are writing it, giving them more brain 
power for the actual content creation.

Decoupling content and format also means that any older document, even one that 
hasn't been touched in years, will be automatically updated to the latest 
format/layout whenever the format/layout is updated, since their content has not 
changed (more on this later).

#### Specification

Once the content has been created by the editors, my goal is to provide a system 
that will take that "raw" content, and format it, consistently, into different 
formats that will later be published. A choice format is of course PDF, but we 
can also convert to Microsoft Word format, HTML (create a website automatically 
for our documentation), EPUB (books that can be read easily on readers/mobile), 
you-name-it.

Here is a non-exhaustive list of the **output** format supported by my proposed 
implementation as of today (even more **input** formats are available):

> Markdown, CommonMark, PHP Markdown Extra, GitHub-Flavored Markdown, MultiMarkdown, 
reStructuredText, XHTML, HTML5, LaTeX (including beamer slide shows), ConTeXt, RTF, 
OPML, DocBook, OpenDocument, ODT, Word docx, GNU Texinfo, MediaWiki markup, DokuWiki 
markup, ZimWiki markup, Haddock markup, EPUB (v2 or v3), FictionBook2, Textile, 
groff man pages, Emacs Org mode, AsciiDoc, InDesign ICML, TEI Simple, and Slidy, 
Slideous, DZSlides, reveal.js or S5 HTML slide shows. It can also produce PDF 
output on systems where LaTeX, ConTeXt, or wkhtmltopdf is installed.

The output should be:

* Consistent across builds: the same content must **always** yield the same result, 
even on different computers, operating systems, or software versions;
* Uniformly formatted: **all** the documents in the library should have the same 
general layout, giving all documentation published by the 132^nd^ Virtual Wing a visual identity 
of their own;
* Retroactively managed: all documents that have been published in the past should 
be **updated without human intervention**. If a logo changes, if we decide to 
change the title page, or the space after paragraphs, those changes should be 
**automatically propagated across the entire library**;
* Adapted to our needs: the documentation should not look "generic" or bland; 
each document should bear a distinct *132nd touch*, and that *touch* should be 
found on **every** document produced by the 132^nd^ Virtual Wing;
* Interlinked: a reference to a document in another document should always
point to that target document, even if it is updated.

## Pros and cons

This section objectively (as much as I could) describes the pros and cons 
of the method I propose to implement.

### The cons

Allow me to start with the cons, and provide, for each of them, a way to 
mitigate them.

#### No WYSIWYG ("What you see is what you get")

In my current proposition, I plan to use the Markdown syntax to write the 
actual content. Markdown is (very) simple; it's pretty much pure text, and 
very similar to the syntax we're using for the forum. Since Markdown is pure 
text, an editor who is busy writing documentation does not see the result 
appear as he types. Font does not resize for headings, pictures do not appear, 
tables look very "raw", etc.

##### Mitigation

* Converting from Markdown to Word/PDF/HTML is trivial, and the tool that 
I will be providing can be installed on any modern computer. Output can 
therefore be refreshed as often as needed to get a "sneak peek" into the 
actual result;
* Numerous WYSIWYG tools exists *online* to edit Markdown. Some of those tools are 
bare editor, providing a side by side "Edit" window and a "Result" window. 
Their offline equivalent are available as well. Moreover, and this gets 
really interesting, Markdown is mature enough that many *free* online editors 
offer amazing synchronization capabilities with Google Drive, Dropbox, 
Github, ..., **effectively allowing anyone to work on any document from any 
computer connected to the web, and directly sends their work for review into 
the Github repository of the 132^nd^ Virtual Wing**.

#### Less liberty when it comes to customizing the format/layout

Having a common template for the layout/format of our document effectively 
"castrates" editors, denying them the liberty to get creative with the way 
their content is rendered. This could get on the nerves on some, especially 
the most perfectionists among us.

##### Mitigation

* In my current proposition, the rendering, formatting and layout is done by 
a professional (although free) typesetting application that has been in 
existence since 1985: [Latex](https://en.wikipedia.org/wiki/LaTeX). 32 years 
of development, testing and improvements have made it quite robust. It has 
been in use for decades by the scientific and teaching community all around 
the world for papers, essays, reports, etc. Even if we might disagree with 
some of the minor formatting choices it makes when it comes to typesetting 
the document (I sometimes do myself, with the placement of pictures for example), 
we can at least be sure that the standard it follows is accepted world-wide, 
and is the result of decades of professional work;
* The layout/format will be 100% identical for all documentation published by 
the 132^nd^ Virtual Wing, branding our documents with a unique "personality", and giving an 
overall "neat" picture of the Wing to the external world;
* In case it becomes necessary, when part of the output does not fit a specific 
need of ours, we can take advantage of the maturity of the tools and customize 
every little detail to our needs.

#### Resources like pictures are to be included on the side

All the files that are to appear in the final document will be referenced in 
Markdown as links only, pointing to a file that exists near the Markdown 
source document (I'll come back on the structure later), or to a website 
for example `http://www.website.com/my_cool_picture.png` is perfectly
valid).
To give an example, if I wanted to include a file named `picture.png` in a 
document named `index.md`, I would have to write the following in `index.md`: 

```
[Picture caption](picture.png)
```

"Picture caption" simply describes the picture, and can be any text. 

"picture.png" is the file itself. My implementation proposition will
scan multiple "media" folders, first the one next to document, then the one
in the parent directory, then the parent of the parent, etc. until it
finds the piture it's looking for. That solution allows us th "share"
pictures between documents. But more on that later!

A neat thing is that picture are automatically resized depending on
a document size; we might want the same document to be created in A3,
A4 and A6, but what of the picture? The same picture would appear tiny
in A3, and overflow the page in A6. With this implementation, pictures
are automatically resized to take approximately 80% of the width of the
page.

##### Mitigation

* Declaring pictures by name offers a finer grained controls on their 
size, and allow for dynamic resizing of pictures from all origins: one 
could, instead of providing a picture file in the `media` folder and 
give its name, include an arbitrary URL, for example: 
`[My cool picture](https://www.all-about-atc.com/the_pattern.png)`. 
The system is very flexible;
* Updating pictures can be done without even opening the source. 
A file named `picture.png` will be included in the final document, 
whatever that file contains. Updating batch of pictures is thus 
very easy, and does not require updating them one by one in every 
Word document (imagine how easy it would be to be able to run batch 
updates on the pictures' library ...);
* Pictures are automatically indexed and referenced in the final document, 
and an automatic "Table of figures" is automatically generated, with 
hyperlinks to the pictures within the text;
* Pictures (and other media) are shared across document (if we want to). 
There is a `media` folder per document, containing pictures that are 
relevant to that specific document only. Then there is a `media` folder 
for the 696^th^ TURNSKINS (for example), which contains all media relevant to the 
696^th^ TURNSKINS and is accessible to all documents of the 696^th^ TURNSKINS. And, finally, 
there is a "root" `media` folder, that contains pictures shared across 
*all* documents (for example, the squadrons logos). If a logo picture 
is updated (for any reason, this is just an example), updating the 
picture file in the root folder would propagate to *all* the documents 
of the 132^nd^ Virtual Wing, updating that picture in each one of them **in a 
completely automated way**.


#### New technologies

While all the cons so far are of relatively small import, I fear this 
one might raise the most shields in our community. Please bear with 
me for a little while?

For this project, I plan on using two pieces of software for the 
front-end (the parts people are expected to interact with): **Markdown** 
and **Git**. For more information about them, see the "Technical" 
section of this document.

**(for information only)**
The back-end, which editors should never interact with (unless they 
want to), consists of **Python**, **Pandoc**, **MikTex**, **Latex**, 
**Appveyor**, and a whole bunch of code. I will not be 
talking about those in this document.

##### Mitigation

While switching to new software always implies somewhat of a 
**learning curve**, I used the following criteria to select them:

  * Free (as in *no dinero*);
  * Open source;
  * Mature;
  * Widely used across the world;
  * Well documented;
  * Will be supported for years to come;
  * Easy enough for the intended usage;
  * Has a luxuriant and flourishing ecosystem of tools around them;
  * Resilient.

The initial learning curve should be very much dampened by the *huge* 
amount of documentation around both *Markdown*, and *Git/Github*. 
Tutorials and documentation is all over the web, and, more importantly, 
**mistakes are free**. Even if someone completely nukes all our 
documentation (and the chances for that to happen are almost none) 
while toying around trying to learn, it can be restored in seconds.

In its simplest form, creating a document would simply be:

1. Download the Github Desktop application
2. Clone our documentation repository
3. Make some changes using Notepad++
4. Commit those changes to a branch
5. Push that branch
6. Signal a repository admin that changes are available
(or create a Pull Request if the editor feels really brave...)

As some of us can already attest, while frightening in the beginning,
this is far from rocket science.

### The pros

This section explains why I'm making this proposal in the first place.

#### Intro: the build process

Before I can present you with examples, I need to explain a few basics 
about the build process I'm proposing.

##### The document folder

Every document lives in its own folder, and is composed of three parts:

![Document folder \label{doc_folder}](https://www.planttext.com/plantuml/img/ROzB2W8n343tEKNe0GfwWbcuzGnIsZW4-XdI51IPkrix3kF2RF9vZuHCLPreIn50MIFXfVYMA2lUImma05j6imE3hc8jJJpX2x37Rbmfi1iuVQel7GRtpMPXhqteP9Syc__iVB0L3bf9bVDidobkvyNV-kp7u1peOLCOU3Im0aoKG__j3G00)

###### **index.md**: the document ("md": "Markdown")

This file contains the actual text of the document.

It can also contains references to other Markdown files, in order
to "include" them, for example the [132-617- SOP](https://www.dropbox.com/s/u9gu9x5hayaht9g/132%20617th%20SOP%202.1.pdf?dl=0) "include"
the [132-617-Quick Reference](https://www.dropbox.com/s/qsbxb2zao9dlpqc/132-617th-%20Quick%20Reference%202.0.pdf?dl=0).


###### **settings.yml**: the document's settings ("yml": "YAML")

This file contains the settings for the document, for example:
* aliases  
* paper size
* references
* title
* etc...

**aliases** are a neat way to create a placeholder for a "complicated", or 
rather long text.For example:

```
aliases:
  - //jf: "J-TAC/FAC(A)"
```

would let us write `// jf` in our "index.md" file, and they would
be automatically replaced by "J-TAC/FAC(A)" in the final document.
It just saves a lot of typing and help reduce typos.

It also help us to have a more "uniform" rendering of the names & conventions
within the 132^nd^ Virtual Wing: for example, I'm using this setting in my "settings.yml":

```
aliases:
  132^nd^ Virtual Wing: 132^nd^ Virtual Wing
```

Whenever I want to reference the Wing, I type `// wing`. If everyone does that,
then we have one and only one way to "express" a given thing.

**Papersize** is a list of formats we'd like to create this document in, 
for example:

```
papersize:
  - a4
  - a5
```

would automatically create two specific PDFs, one in A4, and one in A5.

**references** is a neat way to create a "bibliography" of documents.

For example, here's a piece of mine so far:

```
references:
  // ttp1: "132-TTP-1 CAS Manual, https://www.dropbox.com/..."
  // ttp1a: "132-TTP-1-A CAS Formats, https://www.dropbox.com/..."
  // ttp4: "132-TTP-4 Brevity, https://www.dropbox.com/..."
  // ttp5: "132-TTP-5-ATC and Airbase operations, https://www.dropbox.com/..."
  // ttp6: "132-TTP-6 SCAR, https://www.dropbox.com/..."
  // ttp7: "132-TTP-7 Flight Lead, https://www.dropbox.com/..."
  // ttp8: "132-TTP-8 Briefing Guide, https://www.dropbox.com/..."
  // ttp9: "132-TTP-9-Range Control Officer, https://www.dropbox.com/..."
  // ttp10: "132-TTP-10-AWACS Procedures, https://www.dropbox.com/..."
```

(I removed the full links because they're not needed for this example)

This works the same way as "aliases": if I type `// ttp1` in my document, it will insert a
clickable hyperlink to the document I'm referencing.

If, later, that document's link changes for some reason, there is no need to manually
update all other documents that reference it; all we need to do is update "settings.yml",
re-build the library, and the link is magically updated everywhere.

###### **media** is a folder that contains the images for this document.

If I want to include a picture that is in "media/picture1.png", all I need 
to do is type the following in my "index.md":

```[My picture cool name](picture1.png)```

All the rest (layout & formatting) is automatically taken care of
for me.

Also, if I want to change that picture later, I do not need to edit
my document; overwriting the old picture with the new one will do!


##### The "root" folder

A "document folder" will "live" inside a "root folder" (it's just the 
directory that "contains" the "document folder").

![Root folder \label{root_folder}](https://www.planttext.com/plantuml/img/RLBB2i8m4BpdAq8_e505lVRWLV3WlOHaRGDvbCqMAj9_jwQfVMWkOMScExj3oa02gRE6CT9aWDyRuEWzyOSt2f2nwURPJI0uuaeZIFBupBW8l9t05-FZcPLNK5giwCf-W2IAGZqQPSRNlZWUdCfRLsT_o5DnfcOX1xRG0OYqg_EdDRDHDMARCUvWMoC8GbHGggf4xwUP-PoWtpnOUwVE5oyx-zbx0g8y-0ubhDl-fB6FOJ5ljQGEeTWcySCVjlomMs4VIa3v3MLHQQUWpwsAabYa3GTMWbFZLtW3)

We can see similarities between the "root folder" and the "document folder":

* Both of them contains a "settings.yml" file
* Both of them contains a "media" folder

Put simply, a "root folder" will "share" its settings and its pictures withall its "children"
documents. That allows us to re-use pictures, and declare settings "globally".

For example, we do want to share aliases between documents. Or we might want
to share the GRG map that Looney made between documents.

A very neat feature of that architecture is that updating a setting
or a picture in the "root folder" will update it for *all its
children documents*, in one fell swoop. No need to manually edit
dozens of documents if we decide to change a logo or a name.

**Note**: if the same setting, or the same picture, is declared
in both the "document folder" and the "root folder", then the one
closest to the document will take precedence. That allows us to
"replace" pictures or settings on a per-document basis.

In addition to those three parts, there are also the global settings 
and the global media folder. Those are simply settings and pictures 
that are shared with *all* the documents.

**template.tex**

This file is the "blueprint" that is used to create PDFs.

It is thanks to it that files "look alike".

It is also the most complex part of the chain; it is
written in Latex, which is definitely not user-friendly.

However, the end-result is *amazing*, and, for that reason,
it is used world-wide to this day for an impressive amount
of application.

Several members of the 132^nd^ Virtual Wing are already using it
to create and publish documents, so I'm not afraid
that no-one would be able to tweak the current template
should something happen to me.

Finally, this structure can be repeated *ad nauseam* if we need to:

![Nested root folders \label{nested}](https://www.planttext.com/plantuml/img/VPBDYiCW58NtFeNa0KArqDbsCTk1MNHVHE-aWZ_1t41ByTrhJKAQA9DDSk_vv1mFEGye0exM488Q3T3B3MZm7kcVDme28TERDhyYW4EgT029FZmQAWRQvoMZJqBJiw0_eBJ8kdr_BN96TF9eZEyyEtAdsjvrJKKyiI-yhM8agpm0edPT-x0cMwIPRTp_2Se_azJ3yfLOFNijSGnmsCOjzEDMZxkBLPBp8iu5R6y4mf0HdAVhBDV2BKoBSDySgWMPNRwz7EsxfMannV5ZaB2tgBUqeuecMDbKmV2IYPNh5Qq5UKsx2gcTWdjhLSRoi6iWaaZEu5JwtLy0)

##### The build process, step by step

**Note**: this section is for information and reference only

1. Gather all media folders
2. Find the closest "template" folder
3. Find the "index.md" file
4. Gather all the settings, giving priority to the closest
5. Process the template
	* Inject the media folders found ealier
	* Write the template to a temporary directory
6. Get a title for the document
	* If it's not in the settings, use the folder name
7. Create the output folder if need be
8. Repease for all paper sizes:
	1. Set the pictures width
	2. If we're using multiple paper formats,
	and this one is not "A4", append the format
	to the output file (ex: "MyPDF_a5.pdf")
	3. Process the text of the document:
		* Replaces aliases
		* Process the pictures
			* Include the pictures with the correct width
			* Check that all pictures that are in the media
			folders are used
		* Process the symbols
		(this one is specific to Latex, I won't explain here)
		* Process the references
			* Gather all references in the documents
			* Replace them in the text by a nice link
			* Add a "References" section at the end of the document,
			linking to all references used throughout it
		* Final processing: final touch to the text
	4. Create the (modified) Markdown text and write it to a temporary directory
	5. Actually create the PDF
	
![Processing \label{processing}](https://www.planttext.com/plantuml/img/TLVRRkCs47tdLmpyq4sAh03VZJvirsswHO4D47I3zgM0GKiZcx142XJbooxoxnrUH4cEumV7EdD83WyFPvJFjU7QD6N1c16cGFZ6ouh-P2fjIfG6TYXHSoEK_4_YsGKPaof367rxMV_zyWki9Iyktn5grUYKHWgDgL7wCW9UGssmsemPorMHeORHCzTsrY6fyk0F1lHfcK-O2TuBRqeB198Z2ifpLAYT6aydCaigkHlT22x6IxFlWg-i2zTeZ92xv58MxK8RmWPfl21jcHki7SE4fqq8NsVJnXE3vy60_jfXviSWiTV9YzURxuqCr_llLgr4QXgDuw44R-AJOVprAlThDMgTHZKwbf0PdfCoSnJt4BRsoXWZAucSfuRE-V6B6-1rpNB6KgwpJivVepeRF5Tale13alHGgGZHOhSteF8Ejmk-x36A2uAcekVHjcYmqe8q3Kfhu4KHpLmd3dPVVnaxwhJdnbBKQK04enofKEf00N701pW9imSEHzGNiczDKgL67Ft1Zfm3uHz1LuaNy2_9EFA3Vu8SiHYi-u6MrS8ObAGVVANyppJxNgHxcn5th5JPYtQ6bqk5uLoWu7BNy1sbictygTH8sT1w5IfxPsasgu9TdPBMoBEBenqaRU-EKuA5Ek8z2DFFvqFPag7IwYWoDvn-qx9-VAqAaNLY6wjPlLTDaS41qHz7KyDEsP5ESrg8VXfH8aDQrXvZQu3VLLcwL8JqvaZBZCg3ynPcHHdjPnysOUzri4A1kNF2CERjGDgvMQo6i2lKbeG9MifSx1fVn3p79ld7uzUdDtvef3tiuW9SNfH4EBbTXXtIt5Iv6cstAPKkQG5LXUBuu3XqC7OMhoDcTXlShdz4ASXMZdFY5x8N5KQbgMQ6FS0MpGbHXcEjQvlgdP1KFdbcTxpdHxki8Jyu3Xrq2SeVUEebzOubMG4vUScgVv_qz6TKwjC3bUrspLohigszljpuUn_Yuzi3GgMwCM1oUy3WL5lkz3OtlNP7ovynSZxbEVeYgDr4s75o2xbInKBDWeyVV-xj8zJr0JfX0nCDObD6fXmWCvgwdOu2gh_dzjS0dqPyEi1d4Pyvl9-x5yGL_21l7Nee1NpxOspG35sAlUXjzAgCzaFMCcigVA53MEjIlI6TXRSYNOFGTq8_ulPcjmxqKr5bf1cs22NFl3dvaOk2R-cYaT4jp-tIXTeAEp2cVvqO9_0d9xOUh5Z7ruXnu4s8HuSPwr7VYKIR1DhKqzf-rNKZIve6qioJ1dQoyLc8pnDurYgb2ndNYvnvu2mIeA9MDSOgS0PHabEX5jyxvY8mbzriJrmVCdMIaRCCd5K2lpM2YWvrq1XSKVLKqcXLmCZMBHSuANr0FNytidWtidmtih9bmbzmxoBtzjPpJ8J7h6t74Pem9tPydhBexeZDM4Wx8lE0B2Ao2CWo8ik0h2AoUkjgEp2s0lleNWiKy9IgYihQbx1Cv3cwcbTngjxkf6guMyzy2L_F7s2zUA3taEI-rnwUsmj2rmzuOrH9PJ-bTuRG8lUwaGUm9shRiDBsheINY9ow1eUQsaL1O4NkkAhALcFQsATFGLZttG4J1qmwOEg0QGVC733hWBa3vXsmSC2Y0vOEM7R0oW4h3xWNDlfyfZpfVuF_0G00)

#### Automation

This is one of the biggest pro in my book. The starting point is a 
raw text file, editable from anyone on with access to the Internet, 
and, from there, PDF documents are automatically created and published. 
Even a full-fledged website if we want to !

The build process is triggered every time a file changes on Github. 
That means we get to see what the PDF would be like every time 
someone creates a commit. This is of course very desirable when we 
are actually publishing the document, but it happens too when 
we're *working* on it?

**Every** commit creates PDF. Those PDF are accessible via Appveyor,
so we can review the output, and discuss about it. The common way to
do this is to create branch and make a "Pull Request" from it 
on Github, then push changes to it,
discuss the changes, change so more, discuss some more, etc... until
everyone is happy with the changes.

**Note**: for those of us who worked with *EMFT*, forget about develop
and the like. The flow I'm pushing for in this case is *much* simpler:
"master" is the official branch, everything else is just a
"proposed change". The Pull Request on Github is a very neat way to "talk"
about the changes before they can make their way into "master".
See: [Github flow vs Gitflow](https://lucamezzalira.com/2014/03/10/git-flow-vs-github-flow/)

Once everyone is happy with the changes, the branch we used for the Pull Request
is "merged" into a special branch, called "master", then deleted.
The "master" branch contains
the official documentation. Every commit made on master is built
and then published for the world to see as PDF. For the time being,
I'm using our FTP to publish the PDFs, but that can happen
pretty much anywhere.

**Note:** using the FTP to host documents is my current idea of the 
implementation, but can be changed very easily. I like the FTP idea 
because it means that the same document will always have the same 
link pointing to it, even between versions, which is very convenient 
for writing briefings, or the documents page of our website.

Automation also gives us a lot of flexibility. Let us say we decide 
to change the font we use for the documentation, and examine the 
two following scenarios:

* First scenario, we're using Word. We need to open each document, 
change the style to use the new font, and hope that all the other 
styles used in the document depend on the main style. We visually 
check for that, and hope we won't miss a line. This will take a 
little bit of time (pun intended) and is very error-prone.
* Second scenario, we're using Markdown. We pull the repo (one click), 
change one line (10 seconds), then push the repo back (one click). 
This change is absolute over the entire document library, every 
single character is guaranteed to have been updated.

This stands not only for the font, but for pretty much everything 
else too. Another use case: the application I'm writing lets us 
define "aliases" for recurrent terms. For example, the words 
"132^nd^ Virtual Wing" can be abbreviated to `// wing` in the 
Markdown text file (which is what I'm actually using in this very 
document). Those aliases can be defined globally and for each 
document in a settings files. If we ever decide to become the 
131^st^ Virtual Wing, all it takes to update *all* the documents 
in the library is to change the alias *once* in the root 
settings file (this is a silly example of course, but you get 
the gist). Another advantage is that we won't have a mix of 
132^nd^ Virtual Wing, 132nd Virtual Wing, 132nd vWing, 132 Wing, 132nd, etc...

The same goes for pictures: imagine we decide to include the 
GRG made by Looney (respect, sir) into the 617^th^ DAMBUSTERS TRP. We drop 
the file "dush_grg.png" into a "media" folder next to our 
markdown, and simply type `[Dusheti GRG](dush_grg.png)` 
in our Markdown text (the part between `[]` is the "caption" of the 
picture). Now every time Looney 
updates his GRG, all there is to do is drop the new file in place 
of the old one, and commit the change. No worries about resizing, 
aligning, formatting, publishing. Pull, change, commit, push, and 
grab a coffee; 2 minutes top, coffee included, worry free.

Now let's take the example above a tad further. Imagine the 765^th^ THE DREAD PANTHERS 
decides to include the GRG too. They move the "dush_grg.png" file 
into the "media" folder of the 132^nd^ Virtual Wing, making it available for 
every document in the library, and include it in their TRP too. 
Now, whenever anyone updates "dush_grg.png" in the root media 
folder, it automatically gets updated in every document that 
uses it. How cool is that ? =)

This integrated and automated publication process also gives us 
a lot of information about everything that is going on, at any 
given time. For example, I could see who modified a specific 
line in a specific document. I could also comment directly on 
*that specific line* and start a discussion about it. I could 
revert a specific set of changes, if it turns out they're not 
as good as we thought. Since every commit is independently 
built, and Git branches are cheap, multiple people can work 
at the same time on different chapters of the same document, 
without ever colliding with each other, and have a immediate 
snapshot of their work every time they push it. Once finished, 
integrating the change set back into the "develop" or "master" 
branch is as simple as a click of the mouse.

A side effect of this system is that absolutely every change 
ever pushed on Github are recorded. Every little one of them 
can be retrieved, analyzed, and reverted if we want to. Which 
is, essentially, free backup.

Finally, hosting the documentation on Github gives everyone 
access to it. Anyone can jump in at any given point, and 
suggest a change, fix a typo, etc. Owners and maintainers 
are responsible for accepting or rejecting those changes, 
but virtually anyone willing to create a Github account 
can turn into a contributor.

**Note:** if it turns out that having our work publicly 
available is a show stopper for some of us, please note 
that Bitbucket offers the same kind of functionality for 
an unlimited number of private repositories. I'm a strong 
advocate of going public, though.

Here is a conceptualised workflow for making changes:

![Basic work flow \label{basic_workflow}](F:\DEV\docs\EDLM proposal\media\image1.png){width="168mm}

#### Unified format

All markdown documents are transformed into PDF with a 
master template. This means that:

* all documents will have the same layout and general 
format, giving them a distinct 132^nd^ Virtual Wing look and feel
* updating the template will reflect the changes on all 
documents (ex: title page format, heading size, paragraph 
spacing, bullet lists format, etc.)
* content and format are decoupled
* metadata like table of content, table of figures, table 
of tables (yes), heading numbers, etc. are automatically 
generated for all documents

Basically, what happens during the conversion is:

1. Grab the settings from the global `settings.yml` file
2. Update those settings with the document `settings.yml` file
    * All settings that were in the global settings are 
	preserved, unless a setting with the same name is 
	declared for the document, in which case the global 
    settings are overwritten
    * All settings present in the document file that are 
	not in the global settings will simply be added
3. Using those settings, pre-process the markdown text 
files; settings may include:
    * aliases to replace some text in the document 
	with predefined string
    * a new title for the document, different from the 
	folder name; maybe some characters you want in the 
	title aren't allowed as a folder name on Windows? 
	**Note**: at the time this proposal were written, 
	those were the only two possible settings; many 
	others will probably come in the future
4. Still using the settings, pre-process the Latex 
template; this will, for example:
    * compute the path to the media file
5. Using the resulting template and markdown text, 
build the final PDF.

Why such a complicated system ?

First, we want to be able to declare and access 
settings that are common to all documents, and are 
susceptible to change in the future (new settings may 
be added later without requiring changing the document 
text, no worries). That is the role of the global 
`settings.yml`.

Then, we also want to be able to create settings that 
are specific to the document itself. Maybe some abbreviations 
are valid only in the scope of a specific squadron ? 
That is the role of the `settings.yml` that is in the 
document folder itself.

With those settings, we are able to pre-process the 
Markdown document. Aliases are replaced withon the 
text, etc.

Finally, we need a global `template.tex` to create PDF. 
That template ensures that all documents received the 
same formatting. But, each document also has specific 
needs: their `media` folder will be at a different 
location, and some other settings may be different too. 
So we also pre-process the template using the current 
settings (and information gathered automatically, like 
the `media` folder path).

We now have a pre-processed Markdown, and a pre-processed 
template. We can use Pandoc to get a PDF out of those 
two, and voila !

### Centralized repository

All documents live in one repository, that is itself 
hosted on Github.

The advantages are plenty:

* Automated recording of all changes
* Automated and constant backup
* The library is accessible to all; everyone can suggest 
a change or add content
* review process greatly facilitated: changes are incremental, 
and their authors are clearly displayed; discussions about 
those changes are centralized around the pull request; merging 
the changes once they are ready is a one-click operation
* concurrent edition: many people ca work on the same 
document at the same time, sharing their progress along 
the way (conflicts are handled on a per-line basis)
* ease of access: editing a document or suggesting a 
change is available in all web browsers
* **internal links and bibliography**: a document may 
include another, which may in turn include another, 
which may in turn ...; this makes it very easy to 
propagate changes in all "sub-documents" to their "parent" 
document (for example, a procedure that is commont to 
the whole 132^nd^ Virtual Wing might be outlined in a dedicated document, 
which will be "included" in most TRPs; updating the 
sub-document would then upgrade all associated TRPs); 
building a bibliography that references all documents 
published by the 132^nd^ Virtual Wing would be automated as well, 
allowing for easier reference to other documents
* media files like pictures, logos, maps, etc. are shared 
across all documents; updating them propagates to 
all documents using them

### Extensibility

Once the content has been created (i.e.: the Markdown 
texts are written), we can output in a lot of different 
formats. This means that if, at any given point in the 
future, we find that we would need to publish books with 
our documentation on the Google Play Store and its Apple 
counter-part, it would take us about 5 minutes of manual 
work. The *content* is there already, all we would need 
to do is add the *output* to the pipeline.

This is of course a silly example, but I think 
extensibility is still a very strong pro.

# Technical

This section describes the tools chain that would 
be used to build and publish the documentation.

## Overview

Despite the vast possibilities that those tools 
permit, with a staggering amount of options, 
configurations and features, the whole process will 
be mostly automated, and the editors/reviewers will 
have to deal with very few technicalities.

## Specific tools

The front-end is what editors will have to work with.

### Markdown

Markdown is a [markup language](https://en.wikipedia.org/wiki/Markup_language) 
widely used across the Internet. Its syntax is simple (similar to 
the syntax we use on our forums) and is meant to be readable. This 
very document is written in Markdown; [click here to see the "raw" 
Markdown text](https://raw.githubusercontent.com/132nd-etcher/docs/develop/EDLM.md).

Excerpt from Wikipedia:

> Markdown is a lightweight markup language with plain text 
formatting syntax. It is designed so that it can be converted 
to HTML and many other formats using a tool by the same name. 
Markdown is often used to format readme files, for writing 
messages in online discussion forums, and to create rich text 
using a plain text editor. As the initial description of Markdown 
contained ambiguities and unanswered questions, many implementations 
and extensions of Markdown appeared over the years to answer these issues.

[Here is a cheat-sheet with the available formatting](https://gist.github.com/jonschlinkert/5854601).

For example, here's the link to this very document in Markdown: 
[https://raw.githubusercontent.com/132nd-etcher/docs/master/EDLM%20proposal/index.md](https://raw.githubusercontent.com/132nd-etcher/docs/master/EDLM%20proposal/index.md)

Since it's hosted on Github, here's the link to it when it's 
automatically represented by it (much nicer already): 
[https://github.com/132nd-etcher/docs/blob/master/EDLM%20proposal/index.md](https://github.com/132nd-etcher/docs/blob/master/EDLM%20proposal/index.md)

#### Why Markdown ?

I selected Markdown mainly because **it decouples the content 
and the format**, but also for the following reasons:

* It's readable and easy to "learn"
* It's used all over the web; tutorials are plenty, and all 
questions have been answered
* It's supported by all the major players
* It's very easy to transform into PDF, HTML, EPUB, RST, Microsoft Word, etc.

#### Try it out

You can try Markdown right now, without installing anything. 
Just head to one of those online editor, and write away:

* [dillinger](http://dillinger.io/) (my favorite)
* [classeur](http://classeur.io/)
* [stackedit](https://stackedit.io/editor#)
* [jbt.github.io/markdown-editor](https://jbt.github.io/markdown-editor/)
* [markdownlivepreview](http://markdownlivepreview.com/)
* [hackmd](https://hackmd.io/)
* [etc...](https://www.google.be/search?q=markdown+online+editor&amp;rlz=1C1GGRV_enBE752BE752&amp;oq=markdown+online+editor&amp;aqs=chrome.0.0j69i61j69i60j69i61j0l2.2135j0j7&amp;sourceid=chrome&amp;ie=UTF-8)

#### Offline editors

If you prefer to work offline, there are tons of editors for Markdown:

* [Notepad++](https://notepad-plus-plus.org/) with [plugins](https://www.google.be/search?q=notepad%2B%2B+markdown)
* [Atom](https://atom.io/) with [plugins](https://www.google.be/search?rlz=1C1GGRV_enBE752BE752&amp;q=atom+markdown)

[And millions others...](https://www.google.be/search?q=markdown+editor+windows)

### [Git](https://git-scm.com/) &amp; [Github](https://github.com/)

This is where things get a little bit hairy. It will seem very 
complicated at first, but I can assure you that after doing it a 
few times it makes a lot of sense and becomes actually quite easy 
(we're in the business of simulating a very complex environment, 
I reckon a few commands won't scare you that much =)).

Here is an [introductory tutorial about Git &amp; Github](https://guides.github.com/activities/hello-world/).

Here is another [tutorial about the Git philosophy, and one way to use it](http://thepilcrow.net/explaining-basic-concepts-git-and-github/).

Please don't be scared by all the commands, there is a GUI application 
that lets you do all those things with a click of the mouse.

I selected Git &amp; Github because it allows for a *outstanding way 
of working together on the same project*. With Git &amp; Github, you can:

* Track *all* the changes, and roll back whichever one you'd like (constant backup of everything)
* Associate changes with their author at a glance
* Collaborative editing (many people can work on the same document at the same time)
* Incremental review process supporting discussion
* Issue tracker
* Allows for a lot of automation under the hood
* Git is the *de facto* Source Control Manager nowadays (alternatives: 
[Subversion](https://subversion.apache.org/), 
[Mercurial](http://hginit.com/); 
[compare them](https://www.google.be/search?q=git+vs+subversion+vs+mercurial))
* Github is the *de facto* hosting website for open source 
Git projects (alternatives: [Bitbucket](https://bitbucket.org/product), 
[Gitlab](https://about.gitlab.com/); 
[compare them](https://www.google.be/search?q=gitlab+vs+github+vs+bitbucket))

**Note:** I'm leaving out alternatives that are not 
open-source, self-hosted and free to use.

### What you'll need

This is the list of what you would have to install 
on your computer in order to be able to work on the documentation.

#### Option 1: work online only

This is absolutely possible. For example, with http://dillinger.io/, 
I'm writing this document in Markdown, I get to have a live preview 
of what I'm writing, and I can push it to Github with one click of 
the mouse. No fuss, no problemo.

#### Option 2: work offline

While option 1 is perfectly fine, you can also decide that you 
need more control of what is going on. In that case, you'll 
need a minimal suite of tools.

##### Edit Markdown

This one is easy: you don't need anything. Markdown is pure 
text, so any text editor will do

##### Work with git &amp; Github

First, make sure you followed 
[this tutorial](https://guides.github.com/activities/hello-world/) 
and are a little bit familiar with Git.

Then install the following:
* [Git for windows](https://git-scm.com/download/win)
* [Github windows client application](https://desktop.github.com/) 
(alternatives: [smartGit](http://www.syntevo.com/smartgit/) 
(my favorite, more complex), [Gitkraken](https://www.gitkraken.com/))

That's it ! Create an account on https://github.com/, 
start your local Git client, and you're ready to rock !

# Transition

Transitioning from the current documentation library to 
EDLM will not be painless, but it should not be painful 
either, nor take an unreasonable amount of time.

I'm providing tools to convert from Word/PDF to Markdown, 
but that process is error-prone. So, far, the issues I've 
been able to identify are:

* The format
    * Tables
    * Lists
* The pictures (the pictures are correctly extracted from 
the Word/PDF document, and put in the media folder, but 
their format and/or positioning might need to be adjusted).
 On a big document, like the 617^th^ DAMBUSTERS SOP, this could take a 
 couple of hours. On more simple documents, it might take 
 only a few minutes.

## Process

The actual transition would happen like this:

1. Freeze the current state of the library (no more 
edition of current Word documents)
2. Convert documents in Markdown
3. Build a sane structure for the new library
 * Place pictures in the correct folder (maybe some of 
 them should be shared between document? Or even maybe 
 with the whole Wing?)
 * Define settings and metadata for the documents 
 (title, authors, ...)
4. Build the new library incrementally, green-lighting 
documents one by one until they all pass QA

In all honesty, I'm unable to give an objective estimate 
of the time this will take, mainly because I don't know 
who will be able to spend time on this. Older documents, 
whose maintainers are gone or inactive, can be updated 
by myself or anyone willing.


## Crash course

I plan on offering crash course with Git/Github/Markdown 
to the people who are interested in it, and to write a 
few pages long tutorial to help to get newcomers started 
as well.

The crash course should take about 30 minutes on TS, 
getting people to install the necessary tools, and get 
started with them ("hands on" tutorial).

The written tutorial would be much of the same, covering 
the installation of tools, the publishing process and a 
little syntax related guidelines.
 
# Closing words
 
 Thank you for reading that huge blob of text, I hope I 
 managed to make sense most of the time.
 
 Now that this proposal is out for review within CMD, 
 the next step, in my opinion, could be one of those two:
 
1. The proposal is rejected by CMD, in which case 
the project dies right here.
2. The proposal is accepted by CMD, and is pushed 
to all IPs for review; I'm suggesting this 
supplementary review step because a lot of our 
documentation is actually written by IPs, it would 
make sense for them to have a say in the matter.
3. Depending on IPs feedback, the project either dies,
is adapated, or adopted.

# Pictures used throughout the document
 
The pictures have been generated using PlantUML 
syntax, thanks to the [Planttext website](http://www.planttext.com).
 
Figure \ref{doc_folder}:
[Document folder](https://www.planttext.com/?text=ROzB2W8n343tEKNe0GfwWbcuzGnIsZW4-XdI51IPkrix3kF2RF9vZuHCLPreIn50MIFXfVYMA2lUImma05j6imE3hc8jJJpX2x37Rbmfi1iuVQel7GRtpMPXhqteP9Syc__iVB0L3bf9bVDidobkvyNV-kp7u1peOLCOU3Im0aoKG__j3G00)

Figure \ref{root_folder}:
[Root folder](https://www.planttext.com/?text=RLBB2i8m4BpdAq8_e505lVRWLV3WlOHaRGDvbCqMAj9_jwQfVMWkOMScExj3oa02gRE6CT9aWDyRuEWzyOSt2f2nwURPJI0uuaeZIFBupBW8l9t05-FZcPLNK5giwCf-W2IAGZqQPSRNlZWUdCfRLsT_o5DnfcOX1xRG0OYqg_EdDRDHDMARCUvWMoC8GbHGggf4xwUP-PoWtpnOUwVE5oyx-zbx0g8y-0ubhDl-fB6FOJ5ljQGEeTWcySCVjlomMs4VIa3v3MLHQQUWpwsAabYa3GTMWbFZLtW3)

Figure \ref{nested}:
[Nested root folders](https://www.planttext.com/?text=VPBDYiCW58NtFeNa0KArqDbsCTk1MNHVHE-aWZ_1t41ByTrhJKAQA9DDSk_vv1mFEGye0exM488Q3T3B3MZm7kcVDme28TERDhyYW4EgT029FZmQAWRQvoMZJqBJiw0_eBJ8kdr_BN96TF9eZEyyEtAdsjvrJKKyiI-yhM8agpm0edPT-x0cMwIPRTp_2Se_azJ3yfLOFNijSGnmsCOjzEDMZxkBLPBp8iu5R6y4mf0HdAVhBDV2BKoBSDySgWMPNRwz7EsxfMannV5ZaB2tgBUqeuecMDbKmV2IYPNh5Qq5UKsx2gcTWdjhLSRoi6iWaaZEu5JwtLy0)

Figure \ref{basic_workflow}: 
[Basic work flow](https://www.planttext.com/?text=RLHBJzmm43vtViKe9v1WrSrof2jK5Yea44Wzz81wy3hUn58IftwKhX3_lJEsivkio27oF3oFx_kI6-U5zQ5h0QoINlHrgx3O61awrNlXjUbHLTeRw_3iuUK2Rvys5xXOBCuBlBw-Iv7r6j_XYv1qnkHQpiroRgxcvXLypBlhtKvPQe_Uc9RwjaQAzWAjwenNrFWTa9vAUB4LZYuySfp2Wt5SRr-WS4YNs1DJPMj2XSLpt-fUvNrYqflQiZLD-g5z4xRuIsrHzrxPdP0gvjOn47HCtccUzBjmMg9N__oqA0yLgyxNkgMDBCtfA4_KYWUC-8xxpFiVjy4T8MM2nMhAIXgfEUdnqDFICQT56hMj3iLDDvYUCIrUGijW_GdA-LXbi3c5vZCju-zaS8wfDt-LHTbGTULYRaKnxZbOl3pxUdx98_3vCaKWqqyAEH2G9S2k4Uui0tOTKCrQODy1GCWrOc83-NgsnflP72zb4u9JajKXTP3u2jVRzIqjgFjWWelCrZO22T_eWJjQT8z3S0tIshuXB3lXYFu2jrRqii4tJR1vg-jQMH09NVWDG9XgloTwFwsEn7IVO9OQ87DyjtbymWdHCQwgjWEe6mQJXuOuUJI0OtHSnoB4N63n9NvPS74Me0zPargPuirzL6ZYRAXsMGL9jHHT5dExFB5N9_PL0HyuxV1C45bMPYVITYOwfctkwJthmuxorB4wTUHMKlFgQRFuPbvfawCHEnxGsAYXDVjb4caypoFb9582f74NY_MOVEeeWM6R9AI1FZ6eslX95yjLsLSiS_fqrVY7uVCnvQVfL4Ph_0ECagFS8vOK14WT8lDZeTmq-ew9Dwglw2_-7m00)

Figure \ref{processing}: 
[Processing](https://www.planttext.com/?text=TLVRRkCs47tdLmpyq4sAh03VZJvirsswHO4D47I3zgM0GKiZcx142XJbooxoxnrUH4cEumV7EdD83WyFPvJFjU7QD6N1c16cGFZ6ouh-P2fjIfG6TYXHSoEK_4_YsGKPaof367rxMV_zyWki9Iyktn5grUYKHWgDgL7wCW9UGssmsemPorMHeORHCzTsrY6fyk0F1lHfcK-O2TuBRqeB198Z2ifpLAYT6aydCaigkHlT22x6IxFlWg-i2zTeZ92xv58MxK8RmWPfl21jcHki7SE4fqq8NsVJnXE3vy60_jfXviSWiTV9YzURxuqCr_llLgr4QXgDuw44R-AJOVprAlThDMgTHZKwbf0PdfCoSnJt4BRsoXWZAucSfuRE-V6B6-1rpNB6KgwpJivVepeRF5Tale13alHGgGZHOhSteF8Ejmk-x36A2uAcekVHjcYmqe8q3Kfhu4KHpLmd3dPVVnaxwhJdnbBKQK04enofKEf00N701pW9imSEHzGNiczDKgL67Ft1Zfm3uHz1LuaNy2_9EFA3Vu8SiHYi-u6MrS8ObAGVVANyppJxNgHxcn5th5JPYtQ6bqk5uLoWu7BNy1sbictygTH8sT1w5IfxPsasgu9TdPBMoBEBenqaRU-EKuA5Ek8z2DFFvqFPag7IwYWoDvn-qx9-VAqAaNLY6wjPlLTDaS41qHz7KyDEsP5ESrg8VXfH8aDQrXvZQu3VLLcwL8JqvaZBZCg3ynPcHHdjPnysOUzri4A1kNF2CERjGDgvMQo6i2lKbeG9MifSx1fVn3p79ld7uzUdDtvef3tiuW9SNfH4EBbTXXtIt5Iv6cstAPKkQG5LXUBuu3XqC7OMhoDcTXlShdz4ASXMZdFY5x8N5KQbgMQ6FS0MpGbHXcEjQvlgdP1KFdbcTxpdHxki8Jyu3Xrq2SeVUEebzOubMG4vUScgVv_qz6TKwjC3bUrspLohigszljpuUn_Yuzi3GgMwCM1oUy3WL5lkz3OtlNP7ovynSZxbEVeYgDr4s75o2xbInKBDWeyVV-xj8zJr0JfX0nCDObD6fXmWCvgwdOu2gh_dzjS0dqPyEi1d4Pyvl9-x5yGL_21l7Nee1NpxOspG35sAlUXjzAgCzaFMCcigVA53MEjIlI6TXRSYNOFGTq8_ulPcjmxqKr5bf1cs22NFl3dvaOk2R-cYaT4jp-tIXTeAEp2cVvqO9_0d9xOUh5Z7ruXnu4s8HuSPwr7VYKIR1DhKqzf-rNKZIve6qioJ1dQoyLc8pnDurYgb2ndNYvnvu2mIeA9MDSOgS0PHabEX5jyxvY8mbzriJrmVCdMIaRCCd5K2lpM2YWvrq1XSKVLKqcXLmCZMBHSuANr0FNytidWtidmtih9bmbzmxoBtzjPpJ8J7h6t74Pem9tPydhBexeZDM4Wx8lE0B2Ao2CWo8ik0h2AoUkjgEp2s0lleNWiKy9IgYihQbx1Cv3cwcbTngjxkf6guMyzy2L_F7s2zUA3taEI-rnwUsmj2rmzuOrH9PJ-bTuRG8lUwaGUm9shRiDBsheINY9ow1eUQsaL1O4NkkAhALcFQsATFGLZttG4J1qmwOEg0QGVC733hWBa3vXsmSC2Y0vOEM7R0oW4h3xWNDlfyfZpfVuF_0G00)

