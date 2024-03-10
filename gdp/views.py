from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure
from django.db import models
from django.shortcuts import render

from gdp.models import GDP


def gdp_index(request):
    """Render the GDP index page.

    Year and count are optional query parameters.
    """

    # Define which year to use
    max_year = GDP.objects.aggregate(models.Max("year"))["year__max"]
    min_year = GDP.objects.aggregate(models.Min("year"))["year__min"]
    year = request.GET.get("year", max_year)

    # Define how many countries to show
    count = int(request.GET.get("count", 10))

    # Collect data for the bar chart
    gdps = GDP.objects.filter(year=year).order_by("-gdp")[:count]
    country_names = [gdp.country for gdp in gdps]
    gdp_values = [gdp.gdp for gdp in gdps]

    cds = ColumnDataSource(data=dict(country_names=country_names, gdp_values=gdp_values))

    # Create the bar chart
    fig = figure(x_range=country_names, height=500, title=f"Top {count} GDPs ({year})")
    fig.title.align = "center"
    fig.title.text_font_size = "1.5em"
    fig.xaxis.major_label_orientation = 1.2
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$0.0a")
    fig.vbar(source=cds, x="country_names", top="gdp_values", width=0.8)
    fig.add_tools(
        HoverTool(
            tooltips=[("Country", "@country_names"), ("GDP", "@gdp_values{,}")],
        )
    )

    # Prepare the chart for rendering
    script, div = components(fig)

    context = {
        "script": script,
        "div": div,
        "years": range(min_year, max_year + 1),
        "selected_year": int(year),
        "count": count,
    }

    if request.htmx:
        return render(request, "partials/gdp-bar.html", context)
    return render(request, "gdp_index.html", context)


def gdp_line(request):
    """Render the GDP multiple lines chart page."""
    # Get the list of countries
    countries = GDP.objects.values_list("country", flat=True).distinct()
    selected_countries = request.GET.getlist("country", ["Lithuania"])[:5]
    colors_list = ["red", "green", "blue", "orange", "purple"][0 : len(selected_countries)]

    year_data = []
    gdp_data = []

    for multiple_country in selected_countries:
        gdps = GDP.objects.filter(country=multiple_country).order_by("year")
        year_data.append([gdp.year for gdp in gdps])
        gdp_data.append([gdp.gdp for gdp in gdps])

    cds = ColumnDataSource(
        data=dict(years=year_data, gdp_values=gdp_data, names=selected_countries, colors=colors_list)
    )

    # Create the line chart
    fig = figure(height=500, title=f"GDP of {', '.join(selected_countries)}")
    fig.title.align = "center"
    fig.title.text_font_size = "1.5em"
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$0.0a")
    fig.multi_line(source=cds, xs="years", ys="gdp_values", line_width=2, legend_group="names", line_color="colors")
    fig.legend.location = "top_left"

    # Prepare the chart for rendering
    script, div = components(fig)
    context = {
        "countries": countries,
        "selected_countries": selected_countries,
        "script": script,
        "div": div,
    }

    if request.htmx:
        # TODO: Add a partial for the line chart or rename existing partial to more generic name
        return render(request, "partials/gdp-bar.html", context)
    return render(request, "line.html", context)
