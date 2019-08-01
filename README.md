### http://toscrape.com/
- **Default** [http://quotes.toscrape.com/](http://quotes.toscrape.com/)
   - [quotes_css.py](tutorial/spiders/quotes_css.py)
   - [quotes_xpath.py](tutorial/spiders/quotes_xpath.py)
- **Scroll** [http://quotes.toscrape.com/scroll](http://quotes.toscrape.com/scroll)
   - [quotes_scroll.py](tutorial/spiders/quotes_scroll.py)
- **JavaScript** [http://quotes.toscrape.com/js](http://quotes.toscrape.com/js)
   - [quotes_js.py](tutorial/spiders/quotes_js.py)
- **Tableful** [http://quotes.toscrape.com/tableful](http://quotes.toscrape.com/tableful)
   - None
- **Login** [http://quotes.toscrape.com/login](http://quotes.toscrape.com/login)
   - [login.py](tutorial/spiders/login.py)
- **ViewState** [http://quotes.toscrape.com/search.aspx](http://quotes.toscrape.com/search.aspx)
   - None
- **Random** [http://quotes.toscrape.com/random](http://quotes.toscrape.com/random)
   - [quotes_random](tutorial/spiders/quotes_random.py)
   - `yield response.follow(next_page, self.parse, dont_filter=True)`
   
### mongodb OK
```mongo
db.quotestoscrape.aggregate([
        {$group: {_id: {text: '$text', author: '$author'}, count: {$sum: 1}, dups: {$addToSet: '$_id'}}},
        {$match: {count: {$gt: 1}}}
]).forEach(function(doc){
    doc.dups.shift();
    db.quotestoscrape.remove({_id: {$in: doc.dups}});
})
```

```mongo
db.quotestoscrape.aggregate([
    {$group: {_id : '$text', count: {$sum : 1}}},
    {$match: {count: {$gt : 1}}}
])
```
