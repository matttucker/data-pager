Polymer('data-pager', {

  ready: function() {
    this.firstPage()
  },


  /**
   * descending:
   * @type {Boolean}
   */
  descending: false,

  /**
   * totalItems: The total number of items to paginate
   * @type {Number}
   */
  totalItems: 0,

  /**
   * firstLabel: first page button label
   * @type {String}
   */
  firstLabel: '<<',

  /**
   * lastLabel: last page button label
   * @type {String}
   */
  lastLabel: '>>',

  /**
   * nextLabel: next page button label
   * @type {String}
   */
  nextLabel: '>',

  /**
   * prevLabel: prev page button label
   * @type {String}
   */
  prevLabel: '<',


  firstPage: function() {
    console.log('first page')
    this.currentpage = 1
    this.pageParams = {
      'descending': this.descending ? 'true' : 'false',
      'limit': this.perpage,
      'page': this.currentpage
    }
    this.direction = 'forward'
    this.updateButtons();
  },

  nextPage: function() {
    this.next(1);
  },

  next: function(numPages) {
    console.log('next pages:'+numPages)
    if (this.bookmarks[1]) {
      this.currentpage += numPages;
      this.pageParams = {
        'bookmark': this.bookmarks[1],
        'descending': this.descending ? 'true' : 'false',
        'limit': this.perpage,
        'skip': 1 + (numPages - 1) * this.perpage,
        'page': this.currentpage
      }

    } else {
      this.currentpage = this.pageCount;
    }

    this.direction = 'forward'
    this.updateButtons();
  },

  prevPage: function() {
    this.prev(1);
  },

  prev: function(numPages) {

    this.currentpage -= numPages;
    if (this.currentpage <= 1) {
      this.firstPage()
      return
    }

    this.pageParams = {
      'bookmark': this.bookmarks[0],
      'descending': !this.descending ? 'true' : 'false',
      'limit': this.perpage,
      'skip': 1 + (numPages - 1) * this.perpage,
      'page': this.currentpage
    }

    this.direction = 'reverse'
    this.updateButtons();
  },

  lastPage: function() {
    this.currentpage = this.pageCount;
    this.pageParams = {
      'descending': !this.descending ? 'true' : 'false',
      'limit': this.perpage,
      'page': this.currentpage
    }

    this.direction = 'reverse'
    this.updateButtons();
  },

  updateButtons: function() {
    console.log('update buttons')
    this.$.first_page_button.disabled = this.currentpage == 1
    this.$.prev_page_button.disabled = this.currentpage == 1
    this.$.last_page_button.disabled = this.currentpage == this.pageCount
    this.$.next_page_button.disabled = this.currentpage == this.pageCount
  },

  setBookmarks: function(backwardBookmark, forwardBookmark, numResults) {
    if (numResults == 0) {
      if (this.direction === 'forward') {
        this.bookmarks[1] = '';
      } else {
        this.bookmarks[0] = '';
      }
      return;
    }
    if (this.direction === 'forward') {
      this.bookmarks = [backwardBookmark, forwardBookmark];
    } else {
      this.bookmarks = [forwardBookmark, backwardBookmark];
    }
  },

  sortResults: function(results) {
    if (this.direction === 'forward') {
      return results;
    } else {
      return results.reverse();
    }
  },

  setTotalItems: function(totalItems) {
    this.totalItems = totalItems;
    this.pageCount = Math.ceil(this.totalItems / this.perpage);
    this.currentRange = this.range();
  },

  currentpageChanged: function() {
    this.currentRange = this.range();
  },

  setPage: function(event, detail, sender) {
    var page = parseInt(sender.dataset.item, 10);
    var numPages = this.currentpage - page;
    if (numPages < 0) {
      this.next(-numPages);
    } else if (numPages > 0) {
      this.prev(numPages);
    }
  },

  range: function() {
    console.log('range')
    var paginations = [];

    var start = this.currentpage - Math.floor(this.rangeSize / 2);

    if (start > this.pageCount - this.rangeSize) {
      start = this.pageCount - this.rangeSize + 1;
    }
    if (start < 1) {
      start = 1;
    }
    var end = start + this.rangeSize - 1;
    if (end > this.pageCount) {
      end = this.pageCount;
    }

    for (var i = start; i <= end; i++) {
      paginations.push(i);
    }
    return paginations;
  },
});