$(function () {
  window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
  }, false);

  window.current_tweet = 0;
  window.tweets = [];
  window.rated_tweets = [];

  var moveTweetCursor = function(diff) {
    if(window.current_tweet + diff < window.tweets.length && window.current_tweet + diff >= 0){
      window.current_tweet += diff;
    }
    highlightCurrentTweet();
  }

  var highlightCurrentTweet = function(){
    window.tweets.forEach(function(tweet){
      tweet.$el.find(".tweet").removeClass("highlighted")
    });
    window.tweets[window.current_tweet].$el.find(".tweet").addClass("highlighted")
  }

  var up = function(e){
    moveTweetCursor(-1);
  }
  var down = function(e){
    moveTweetCursor(1);
  }

  var rankNonRelevant = function(e){
    window.tweets[window.current_tweet].rank(-1)
    down();
  }

  var rankRelevant = function(e){
    window.tweets[window.current_tweet].rank(1)
    down();
  }

  Mousetrap.bind("up", up);
  Mousetrap.bind("down", down);
  Mousetrap.bind("left", rankNonRelevant);
  Mousetrap.bind("right", rankRelevant);

  var processRanking = function(data, textStatus, jqXHR) {
    console.log(data.tweets.length);
    window.current_tweet = 0;
    window.tweets = [];
    window.rated_tweets = [];

    window.url = data.url;
    window.options = data.options;

    data.tweets.forEach(function (tweetObj, i) {
      var tweetView = new TweetView(tweetObj);
      $(".evaluation").append(tweetView.render().el);
      window.tweets.push(tweetView);
    });
    highlightCurrentTweet();
  }

  var TweetView = Backbone.View.extend({
    template : _.template($("#tweet-template").html()),

    initialize: function(data) {
      var tweet = data[1];
      tweet.score = data[0];
      this.tweet = tweet;
    },
    rank: function(score) {
      this.$el.css("transition", "all 1.0s ease-in-out")
      this.$el.css("transform","translateX("+ score * 450+"px)")
      this.$el.fadeOut(300, function(){
        $(this).css({visibility: 'hidden', display:'block'})
                .slideUp(200);
      });

      $.ajax("evaluate", {
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
          url: window.url,
          tweetId: this.tweet._id,
          rating: score,
          options: window.options,
        })
      })
    },
    render: function() {
      this.$el.html(this.template(this.tweet));

      var DRAG_OFFSET = 100;        

      this.$el.draggable({
        axis: "x",
        scroll: false,
        cancel: "p.tweet-body",
        start: function(event, ui) {
            this.originalX = this.offsetLeft;
        },
        stop: function(event, ui) {
            if (!this.reverted) {
                var relevant = this.offsetLeft > this.originalX;
                $.ajax("evaluate", {
                    type: "POST",
                    contentType: "application/json",
                    dataType: "json",
                    data: JSON.stringify({
                        url: window.url,
                        tweet: this.dataset.id,
                        relevant: relevant,
                        options: window.options,
                    }),
                });
                $(this).fadeOut(300, function(){
                    $(this).css({visibility: 'hidden', display:'block'})
                           .slideUp(200);
                });
            }
        },
        revert: function() {
            var that = this[0];
            return that.reverted =
                Math.abs(that.originalX - that.offsetLeft) < DRAG_OFFSET;
        },
        revertDuration: 200,
      });
      
      return this;
    },

  });

  $.ajax("evaluation/next").done(processRanking);

});