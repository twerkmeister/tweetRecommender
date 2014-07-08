$(function () {
  window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
  }, false);

  var up = function(e){
    tweets.moveTweetCursor(-1);
  }
  var down = function(e){
    tweets.moveTweetCursor(1);
  }

  var rankNonRelevant = function(e){
    tweets.rankTweet(-1);
  }

  var rankRelevant = function(e){
    tweets.rankTweet(1);
  }

  Mousetrap.bind("up", up);
  Mousetrap.bind("down", down);
  Mousetrap.bind("left", rankNonRelevant);
  Mousetrap.bind("right", rankRelevant);    

  var TweetModel = Backbone.Model.extend({
    rank: function(score){
      this.trigger("ranked", score);
      $.ajax("evaluate", {
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
          tweetId: this.get("_id"),
          rating: score,
          webpage: this.collection.newsURL
        })
      });
    }

  });

  var TweetsCollection = Backbone.Collection.extend({
    model: TweetModel,
    url: "evaluation/next",
    initialize: function() {
      this.current_tweet=0;
      this.listenTo(this, "sync", function(){
        if(this.length > 0)
          this.at(this.current_tweet).trigger("highlight");
        else
          this.fetchNew();});
    },
    parse: function(response){
      if(response.tweets.length == 0){
        toastr.error("Error calculating a ranking");

      }
      this.newsURL = response.url
      this.newsId = response.newsId
      return response.tweets

    },
    moveTweetCursor: function(diff) {
      if(this.current_tweet + diff < this.length && this.current_tweet + diff >= 0){
        this.current_tweet += diff;
        this.at(this.current_tweet).trigger("highlight")
      }
      else if(this.current_tweet >= this.length && this.length > 0){
        this.current_tweet = this.length -1;
        this.at(this.current_tweet).trigger("highlight")
      }
    },
    rankTweet: function(score) {
      this.at(this.current_tweet).rank(score);
      this.remove(this.at(this.current_tweet));
      this.moveTweetCursor(0);
      if(this.length == 0) {
        if (finished) {
          $("#instructionModal").modal("hide");
          $("#finishModal").modal("show");
        }
        else
          this.fetchNew()
      }
    },
    fetchNew: function() {    
      this.fetch();
    }
  });

  var TweetView = Backbone.View.extend({
    template : _.template($("#tweet-template").html()),
    initialize: function(){
      this.listenTo(this.model, "highlight", this.highlight);
      this.listenTo(this.model, "ranked", this.ranked)
    },
    ranked: function(score) {

      this.$el.on("animationend webkitAnimationEnd", function(e){
        if(e.originalEvent.animationName == "shrink")
          this.remove();
      }.bind(this));
      if(score == 1)
        this.$el.addClass("moveright");
      else
        this.$el.addClass("moveleft");
    },
    render: function() {
      //console.log(this.template(this.model.toJSON()));
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },
    highlight: function() {
      //Disclaimer: This is bad style
      $(".highlighted").removeClass("highlighted");
      this.$el.addClass("highlighted");
    }

  });

  var TweetCollectionView = Backbone.View.extend({
    template: _.template("<div></div>"),
    initialize: function(){
      this.listenTo(this.collection, "sync", function(){
        this.render(); 
        this.collection.first().trigger("highlight");               
      })
      this.collection.fetchNew();      
    },
    render: function() {
      this.$el.html(this.template());
      var self = this;
      this.collection.forEach(function(tweetModel){
        var tweetView = new TweetView({model: tweetModel})
        self.$el.append(tweetView.render().el)
      });      
      return this;
    }
  })

  var ArticleModel = Backbone.Model.extend({
    urlRoot: "article",
    defaults: {
      url: "",
      article: "",
      num_articles: ""
    }
  })
  
  var ArticleView = Backbone.View.extend({
    initialize: function(){
      this.listenTo(this.collection, "sync", function(){
        this.model.set("id", this.collection.newsId);
        this.model.fetch();
      });
      this.listenTo(this.model, "sync", this.render);             
    },
    template : _.template($("#article-template").html()),
    render : function() {      
      this.$el.html(this.template(this.model.toJSON()));
      if (this.model.get("num_articles") == "24")
        finished = true;
      return this;
    },
    events : {'click a.article_toggle' : 'articleToggling'},
    articleToggling : function(e) {
      $(".article_text").slideToggle("slow");
      $(e.currentTarget).text(($(e.currentTarget).text() == 'Show Article') ? 'Hide Article': 'Show Article');
    },  
  });

  $("#instructionModal").modal("show")

  var tweets = new TweetsCollection(); 
  var tweetCollectionView = new TweetCollectionView({collection: tweets});
  var article = new ArticleModel();
  var ArticleView = new ArticleView({collection: tweets, model: article});
  $(".evaluation").append(tweetCollectionView.render().el)
  $(".article").append(ArticleView.render().el)

  var finished = false;

  // if (finished) {
  //   $("#instructionModal").modal("hide");
  //   $("#finishModal").modal("show");
  // }
 
});