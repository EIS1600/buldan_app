d3.tsv("data/prosopData.tsv").then(function(data_csv) {
    var search = d3.select("#search_btn")
    var checker = (arr, target) => target.every(v => arr.includes(v));
    function zFill(num, size) {
        var s = num+"";
        while (s.length < size) s = "0" + s;
        return s;
    }
    search
        .on("click", function (d) {
            var search_term = d3.select("#search_input").property("value");
            var new_id_label = d3.select("#new_id");
            new_id_label.text("");
            var current_date = new Date();
            let new_id = current_date.getFullYear().toString().substr(-2) +
                zFill(current_date.getMonth(), 2) +
                zFill(current_date.getDate(),2) +
                zFill(current_date.getHours(), 2) +
                zFill(current_date.getMinutes(), 2) +
                zFill(current_date.getSeconds(), 2)

            new_id_label.
            text(function() {
                return "new ID: " + new_id;
            })
            if (search_term !== "") {
                var filtered_data = filter_data(search_term);
                var res_container = d3.select("#search_results_div");
                var search_container = d3.select("#search_div");
                // remove tags to be updated
                res_container.selectAll("*").remove();
                search_container.select("#res_cnt").remove();
                // add result count
                search_container
                    .append("h2")
                    .attr("id", "res_cnt")
                    .text(function(e) {
                        return "Matches: " + filtered_data.length.toString() + " result(s)"
                    })
                // add results list
                var new_ul = res_container
                    .append('ul')
                    .selectAll("li")
                    .data(filtered_data)
                    .enter()
                var new_li = new_ul.append("li")
                new_li.append("p")
                    .text(function (d) {
                        return d.ID;
                    })
                    .attr("class", "ID")
                new_li.append("p")
                    .html(function (d) {
                        var name_toks = d.NAME.trim().split(" ");
                        var search_toks_norm = normalize_ar(search_term.trim()).split(" ");
                        var html_str = "";
                        name_toks.forEach(function(tok) {
                            if (search_toks_norm.indexOf(normalize_ar(tok)) !== -1) {
                                html_str = html_str +
                                    " <p style='background-color: #4CAF50; color: white; display: inline'>" + tok +
                                    "</p>";
                            }
                            else {
                                html_str = html_str + " " + tok;
                            }
                        })
                        return " - " + html_str;
                    })
                    .style("display", "inline")
                    .append("a")
                    .attr('href',function (d) {
                        return "data/0900IbnCabdMuncimHimyari.RawdMictar/" + d.ID + ".html";
                    })
                    .attr("target","_blank")
                    .text( function() {
                        return " —> اعرض المزيد";
                    });
            }

        });

    function filter_data(term) {
        let term_toks = term.split(" ");
        return data_csv.filter(
            function(row) {
                let norm_row = normalize_ar(row['NAME']);
                return checker(norm_row,
                    term_toks.map(function(t) {return normalize_ar(t);}));
            });
    }
    function normalize_ar(str) {
        let repl = {
            "[إأٱآا]" : "ا",
            "[يى]ء": "ئ",
            "ي": "ى",
            "(ؤ)": "ء",
            "(ئ)": "ء"
        }
        for (let key in repl) {
            let reg_pat = new RegExp(key, 'g')
            str = str.replace(reg_pat, repl[key]);
        }
        return str;
    }
});
