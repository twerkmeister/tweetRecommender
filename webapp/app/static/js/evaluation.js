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
          url: this.collection.url,
          tweetId: this.get("_id"),
          rating: score,
          options: this.collection.newsURL,
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
          this.fetch();});
    },
    parse: function(response){
      if(response.tweets.length == 0){
        toastr.error("Error calculating a ranking");

      }
      this.options = response.options
      this.newsURL = response.url
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
      if(this.length == 0)
        this.fetch()
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
    	  var articleView = new ArticleView(this.collection.newsURL);    
    	  $(".article").append(articleView.render().el);
      })
      this.collection.fetch();      
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
  

	   var ArticleView = Backbone.View.extend({
		initialize: function(url){
				     this.newsURL = url;      
				     $(".article").empty();				     
		},
		template : _.template($("#article-template").html()),
		render : function() {					
					var that = this
					$.ajax("article", {
						type : "POST",
						contentType : "application/json",
						dataType : "json",
						data : JSON.stringify({
							"url" : this.newsURL
						}),
						success : function(result) {
							that.$el.html(that.template(result));							
						}
					});					
					return this;
				},
		events : {'click a.article_toggle' : 'articleToggling'},
		articleToggling : function(e) {
					$(".article_text").slideToggle("slow");
					$(e.currentTarget).text(($(e.currentTarget).text() == 'Show Article') ? 'Hide Article': 'Show Article');
				 }		
		});

  var tweets = new TweetsCollection();  
  var tweetCollectionView = new TweetCollectionView({collection: tweets});  
  $(".evaluation").append(tweetCollectionView.render().el);
});