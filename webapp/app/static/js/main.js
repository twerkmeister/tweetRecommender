$(function () {

  var processRanking = function(data, textStatus, jqXHR) {
    console.log(data.tweets.length);
    data.tweets.forEach(function (tweetObj, i) {
      var tweetView = new TweetView(tweetObj);
      $(".search").append(tweetView.render().el);
    });
  }

  var TweetView = Backbone.View.extend({
    template : _.template($("#tweet-template").html()),

    initialize: function(tweet) {;
      this.tweet = tweet;
    },
    render: function() {
      this.$el.html(this.template(this.tweet));
      
      return this;
    },

  });
  

  var OptionSetView = Backbone.View.extend({

    template : _.template($("#optionset-template").html()),

    initialize : function (options) {
      this.data = options.data;
    },

    render : function () {

      this.$el.html(this.template(this.data));

      //setting defaults
      this.$("option[name=\"gatheringMethods[terms]\"]")[0].selected = true
      this.$("input[name=\"rankingMethods[text_overlap]\"]").prop("checked", true);
      this.$("input[name=\"filteringMethods[expected_time]\"]").prop("checked", true);

      return this;
    },

    toggle : function () {
      this.$el.toggle();
    },


    foldCheckboxes : function (options, key) {
      return _.transform(
        options[key], function (result, value, key) { 
          if (value) 
            result.push(key); 
        }, []
      );
    },

    serialize : function () {
      var options = Backbone.Syphon.serialize(this);
      options.filteringMethods = this.foldCheckboxes(options, "filteringMethods");
      options.rankingMethods = this.foldCheckboxes(options, "rankingMethods");
      return options;
    },


    query : function () {

      var options = this.serialize();
      options["url"] = $("#searchbar")[0].value;

      return $.ajax("query", {
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(options)
      });
    }

  });

  $.ajax("options").done(function(data) {

    var view = new OptionSetView({
      data : data
    });
    $(".search").append(view.render().el);
    $(".optionset").toggle();



    $("#searchbutton").click(function() {

      $(".tweet").remove();
      view.query().done(processRanking);

    });

    $("#randombutton").click(function() {
      $.ajax("url").done(function(data){
        $("#searchbar")[0].value=data["url"];
      });
    });


    $("#advancedbutton").click(function(){
      $(".optionset").toggle();
    });

    window.options = view;

  });

});