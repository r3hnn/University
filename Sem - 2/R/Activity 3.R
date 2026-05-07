library(shiny)
library(ggplot2)

ui <- fluidPage(
  tags$head(tags$style(HTML(" @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap'); *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; } body { background: #f0f2f8; font-family: 'Inter', sans-serif; font-size: 14px; color: #1e2235; min-height: 100vh; } .navbar-custom { background: #ffffff; border-bottom: 1px solid #e8ebf5; padding: 0 36px; display: flex; align-items: stretch; height: 58px; position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 12px rgba(30,34,53,0.06); } .navbar-brand-area { display: flex; align-items: center; gap: 10px; margin-right: 40px; } .brand-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #4f7ef8, #7b5cf0); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; } .brand-title { font-size: 15px; font-weight: 700; color: #1e2235; letter-spacing: -0.3px; } .brand-sub { font-size: 11px; color: #9ba3bf; font-weight: 400; } .nav-tabs { border: none !important; display: flex; align-items: stretch; height: 100%; margin: 0 !important; background: transparent; } .nav-tabs > li { margin: 0 !important; display: flex; align-items: stretch; } .nav-tabs > li > a { border: none !important; border-bottom: 2px solid transparent !important; background: transparent !important; color: #8a93b0 !important; font-size: 13px !important; font-weight: 500 !important; padding: 0 18px !important; display: flex !important; align-items: center !important; height: 58px !important; border-radius: 0 !important; transition: color 0.2s, border-color 0.2s; } .nav-tabs > li.active > a, .nav-tabs > li > a:hover { color: #4f7ef8 !important; border-bottom: 2px solid #4f7ef8 !important; background: transparent !important; } .tab-content { display: none !important; } .page-grid { display: grid; grid-template-columns: 280px 1fr; gap: 20px; align-items: start; } .sidebar-card { background: #ffffff; border-radius: 14px; border: 1px solid #e8ebf5; box-shadow: 0 2px 16px rgba(30,34,53,0.05); padding: 24px; } .sidebar-section { margin-bottom: 6px; } .sidebar-section-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #b0b8d4; margin-bottom: 14px; margin-top: 22px; padding-top: 22px; border-top: 1px solid #f0f2f8; } .sidebar-section-title:first-child { margin-top: 0; padding-top: 0; border-top: none; } .form-group { margin-bottom: 14px !important; } label:not(.file-upload-wrapper label) { font-size: 12px !important; font-weight: 500 !important; color: #6b748f !important; margin-bottom: 6px !important; display: block !important; } input[type='text']:not(.selectize-input input), input[type='number'], select, .form-control:not(.selectize-control) { background: #f7f8fc !important; border: 1.5px solid #e4e8f5 !important; border-radius: 8px !important; color: #1e2235 !important; font-family: 'Inter', sans-serif !important; font-size: 13px !important; padding: 9px 12px !important; width: 100% !important; transition: border-color 0.18s, box-shadow 0.18s !important; height: 38px !important; } .selectize-input { background: #f7f8fc !important; border: 1.5px solid #e4e8f5 !important; border-radius: 8px !important; color: #1e2235 !important; font-family: 'Inter', sans-serif !important; font-size: 13px !important; padding: 0 12px !important; width: 100% !important; transition: border-color 0.18s, box-shadow 0.18s !important; min-height: 38px !important; display: flex !important; align-items: center !important; box-shadow: none !important; } .selectize-input > input { border: none !important; background: transparent !important; box-shadow: none !important; outline: none !important; padding: 0 !important; height: auto !important; margin: 0 !important; } input[type='text']:not(.selectize-input input):focus, input[type='number']:focus, select:focus, .form-control:not(.selectize-control):focus, .selectize-input.focus { border-color: #4f7ef8 !important; outline: none !important; box-shadow: 0 0 0 3px rgba(79,126,248,0.12) !important; background: #ffffff !important; } input[type='radio'] { accent-color: #4f7ef8; } .radio label, .radio-inline label { color: #4a5270 !important; font-size: 13px !important; font-weight: 400 !important; } .help-block { color: #b0b8d4 !important; font-size: 11px !important; font-family: 'JetBrains Mono', monospace !important; margin-top: 5px !important; line-height: 1.4 !important; } .file-upload-wrapper { width: 100%; } .file-upload-wrapper .input-group { display: flex !important; align-items: center !important; width: 100% !important; gap: 0 !important; } .file-upload-wrapper .btn-file { background: #4f7ef8 !important; border: none !important; border-radius: 8px 0 0 8px !important; color: #fff !important; font-size: 12px !important; font-weight: 600 !important; font-family: 'Inter', sans-serif !important; padding: 9px 14px !important; height: 38px !important; white-space: nowrap !important; cursor: pointer !important; flex-shrink: 0 !important; display: flex !important; align-items: center !important; } .file-upload-wrapper .btn-file:hover { background: #3a6de0 !important; } .file-upload-wrapper .form-control[readonly] { border-radius: 0 8px 8px 0 !important; border-left: none !important; background: #f7f8fc !important; color: #8a93b0 !important; font-size: 12px !important; height: 38px !important; flex: 1 !important; min-width: 0 !important; } .shiny-input-container:has(input[type='file']) { width: 100% !important; } .btn { font-family: 'Inter', sans-serif !important; font-size: 13px !important; font-weight: 600 !important; border-radius: 8px !important; padding: 9px 16px !important; width: 100% !important; cursor: pointer !important; transition: all 0.18s !important; border: none !important; height: 38px !important; display: flex !important; align-items: center !important; justify-content: center !important; margin-top: 8px !important; } .btn-primary { background: linear-gradient(135deg, #4f7ef8, #7b5cf0) !important; color: #fff !important; box-shadow: 0 3px 12px rgba(79,126,248,0.3) !important; } .btn-primary:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 18px rgba(79,126,248,0.4) !important; } .btn-default { background: #f0f2f8 !important; color: #6b748f !important; border: 1.5px solid #e4e8f5 !important; } .btn-default:hover { background: #e8ebf5 !important; color: #4f7ef8 !important; border-color: #4f7ef8 !important; } .main-card { background: #ffffff; border-radius: 14px; border: 1px solid #e8ebf5; box-shadow: 0 2px 16px rgba(30,34,53,0.05); padding: 26px; } .card-title { font-size: 15px; font-weight: 700; color: #1e2235; margin-bottom: 4px; } .card-sub { font-size: 12px; color: #9ba3bf; margin-bottom: 20px; } .section-divider { border: none; border-top: 1px solid #f0f2f8; margin: 22px 0; } .col-tags-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; } .col-tag { background: #eef2ff; color: #4f7ef8; border: 1px solid #d4dffd; border-radius: 20px; padding: 3px 10px; font-size: 11px; font-family: 'JetBrains Mono', monospace; font-weight: 500; } .col-tag-cat { background: #fff4ee; color: #f07a3a; border: 1px solid #fddec8; border-radius: 20px; padding: 3px 10px; font-size: 11px; font-family: 'JetBrains Mono', monospace; font-weight: 500; } .table-box { border: 1px solid #e8ebf5; border-radius: 10px; overflow: hidden; overflow-x: auto; } table { width: 100% !important; border-collapse: collapse !important; font-size: 13px !important; } thead th { background: #f7f8fc !important; color: #6b748f !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.07em !important; padding: 11px 16px !important; border-bottom: 1px solid #e8ebf5 !important; text-align: left !important; } tbody td { padding: 10px 16px !important; color: #3a4060 !important; border-bottom: 1px solid #f4f5fb !important; font-size: 13px !important; } tbody tr:last-child td { border-bottom: none !important; } tbody tr:hover td { background: #f7f9ff !important; } .info-note { background: #eef2ff; border: 1px solid #d4dffd; border-radius: 8px; padding: 10px 14px; font-size: 12px; color: #3a5fd4; margin-bottom: 16px; font-family: 'JetBrains Mono', monospace; } .stat-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px; } .stat-card { background: #f7f8fc; border: 1px solid #e8ebf5; border-radius: 10px; padding: 16px; text-align: center; } .stat-card .s-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #9ba3bf; margin-bottom: 6px; } .stat-card .s-value { font-size: 22px; font-weight: 700; color: #4f7ef8; } .plot-outer { background: #f7f8fc; border: 1px solid #e8ebf5; border-radius: 10px; padding: 8px; } .empty-state { text-align: center; padding: 60px 20px; color: #b0b8d4; } .empty-state .e-icon { font-size: 40px; margin-bottom: 12px; } .empty-state .e-text { font-size: 14px; font-weight: 500; color: #9ba3bf; } .empty-state .e-sub { font-size: 12px; color: #b0b8d4; margin-top: 4px; } pre { background: #f7f8fc !important; border: 1px solid #e8ebf5 !important; border-radius: 10px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important; color: #3a4060 !important; padding: 16px !important; } .well { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; } .shiny-input-container { margin-bottom: 14px !important; } select { appearance: auto !important; } "))),
  tags$script(HTML("
    Shiny.addCustomMessageHandler('clearFileDisplay', function(msg) {
      var d = document.getElementById('csv_file_display');
      if (d) d.value = 'No file chosen';
      var f = document.getElementById('csv_file_real');
      if (f) f.value = '';
    });
  ")),

  # ── Navbar ────────────────────────────────────────────────────────────────
  div(class = "navbar-custom",
    div(class = "navbar-brand-area",
      div(class = "brand-icon", "📊"),
      div(
        div(class = "brand-title", "EduAnalytics"),
        div(class = "brand-sub",   "Student Performance Dashboard")
      )
    ),
    tabsetPanel(
      id = "main_tabs",

      # ── Tab 1: Data ──────────────────────────────────────────────────────
      tabPanel("📁  Data",
        div(style = "height:32px;")
      ),
      tabPanel("📈  Visualise",
        div(style = "height:32px;")
      ),
      tabPanel("🧹  Data Cleaning",
        div(style = "height:32px;")
      )
    )
  ),

  # ── Tab content ───────────────────────────────────────────────────────────
  div(style = "padding: 28px 36px;",
    uiOutput("tab_content")
  )
)


server <- function(input, output, session) {

  # ── Data store ─────────────────────────────────────────────────────────────
  reset_count <- reactiveVal(0)
  cleaned     <- reactiveVal(NULL)
  stats_data  <- reactiveVal(NULL)

  rv_stu <- reactiveVal(data.frame(
    student     = character(),
    study_hours = numeric(),
    Marks       = numeric(),
    Attendance  = numeric(),
    stringsAsFactors = FALSE
  ))

  observeEvent(input$csv_text, {
    req(input$csv_text)
    df <- read.csv(text = input$csv_text, stringsAsFactors = FALSE)
    rv_stu(df)
    cleaned(NULL)
    stats_data(NULL)
  })

  observeEvent(input$add_student, {
    req(input$stu_name)
    new_row <- data.frame(
      student     = input$stu_name,
      study_hours = input$stu_hours,
      Marks       = input$stu_marks,
      Attendance  = input$stu_attend,
      stringsAsFactors = FALSE
    )
    rv_stu(rbind(rv_stu(), new_row))
    cleaned(NULL)
    stats_data(NULL)
    updateTextInput(session, "stu_name", value = "")
    for (id in c("stu_hours", "stu_marks", "stu_attend")) updateNumericInput(session, id, value = NA)
  })

  observeEvent(input$reset_stu, {
    rv_stu(data.frame(
      student     = character(),
      study_hours = numeric(),
      Marks       = numeric(),
      Attendance  = numeric(),
      stringsAsFactors = FALSE
    ))
    cleaned(NULL)
    stats_data(NULL)
    reset_count(reset_count() + 1)
    session$sendCustomMessage("clearFileDisplay", list())
  })

  # ── Column detection ───────────────────────────────────────────────────────
  detect_cols <- reactive({
    df   <- rv_stu()
    cols <- colnames(df)
    list(
      name_col     = cols[sapply(cols, function(c) is.character(df[[c]]) || is.factor(df[[c]]))][1],
      numeric_cols = cols[sapply(cols, function(c) is.numeric(df[[c]]))],
      has_marks    = any(grepl("mark|score|grade|result", cols, ignore.case = TRUE)),
      has_hours    = any(grepl("hour|study|time",         cols, ignore.case = TRUE)),
      has_attend   = any(grepl("attend|presence",         cols, ignore.case = TRUE)),
      has_gender   = any(grepl("gender|sex",              cols, ignore.case = TRUE)),
      has_parent   = any(grepl("parent|education|level",  cols, ignore.case = TRUE)),
      marks_col    = cols[grepl("mark|score|grade|result", cols, ignore.case = TRUE)][1],
      hours_col    = cols[grepl("hour|study|time",         cols, ignore.case = TRUE)][1],
      attend_col   = cols[grepl("attend|presence",         cols, ignore.case = TRUE)][1],
      gender_col   = cols[grepl("gender|sex",              cols, ignore.case = TRUE)][1],
      parent_col   = cols[grepl("parent|education|level",  cols, ignore.case = TRUE)][1]
    )
  })

  # ── Tab content router ─────────────────────────────────────────────────────
  output$tab_content <- renderUI({
    tab <- input$main_tabs
    if (is.null(tab) || tab == "📁  Data") {
      data_tab_ui()
    } else if (tab == "📈  Visualise") {
      visualise_tab_ui()
    } else {
      cleaning_tab_ui()
    }
  })

  # ── DATA TAB UI ────────────────────────────────────────────────────────────
  data_tab_ui <- function() {
    div(class = "page-grid",

      # Sidebar
      div(class = "sidebar-card",

        div(class = "sidebar-section-title", "Upload CSV"),
        div(class = "file-upload-wrapper",
          uiOutput("file_input_ui")
        ),
        tags$p(class = "help-block", "Any CSV with student columns"),

        div(class = "sidebar-section-title", "Manual Entry"),
        textInput("stu_name",    "Student Name",   value = "", placeholder = "e.g. Alice"),
        numericInput("stu_hours",  "Study Hours",    value = NULL),
        numericInput("stu_marks",  "Marks",          value = NULL),
        numericInput("stu_attend", "Attendance (%)", value = NULL),
        actionButton("add_student", "➕  Add Student", class = "btn btn-primary"),

        div(class = "sidebar-section-title", "Actions"),
        actionButton("reset_stu", "↺  Reset Data", class = "btn btn-default")
      ),

      # Main
      div(class = "main-card",
        div(class = "card-title", "Student Records"),
        div(class = "card-sub",   "Data loaded from CSV upload or manual entry"),

        uiOutput("col_tags_ui"),

        uiOutput("data_table_or_empty")
      )
    )
  }

  # ── VISUALISE TAB UI ───────────────────────────────────────────────────────
  visualise_tab_ui <- function() {
    div(class = "page-grid",

      div(class = "sidebar-card",
        div(class = "sidebar-section-title", "Chart Type"),
        uiOutput("plot_choices_ui"),
        br(),
        actionButton("plot_stu", "Generate Chart", class = "btn btn-primary")
      ),

      div(class = "main-card",
        div(class = "card-title", "Visualisation"),
        div(class = "card-sub",   "Auto-detects which columns to use for each chart"),
        uiOutput("plot_note_ui"),
        div(class = "plot-outer",
          plotOutput("stu_plot", height = "420px")
        )
      )
    )
  }

  # ── CLEANING TAB UI ────────────────────────────────────────────────────────
  cleaning_tab_ui <- function() {
    div(class = "page-grid",

      div(class = "sidebar-card",
        div(class = "sidebar-section-title", "Mean Imputation"),
        tags$p(style = "font-size:13px; color:#6b748f; line-height:1.6;",
               "Replaces missing values in numeric columns with the column mean."),
        br(),
        actionButton("clean_data", "Apply Imputation", class = "btn btn-primary"),

        div(class = "sidebar-section-title", "Statistics"),
        actionButton("show_stats", "Show Summary Stats", class = "btn btn-primary")
      ),

      div(class = "main-card",
        div(class = "card-title", "Data Cleaning"),
        div(class = "card-sub",   "Mean imputation and summary statistics"),

        uiOutput("stats_cards_ui"),

        div(class = "card-title", style = "font-size:13px; margin-bottom:10px;", "Cleaned Data"),
        div(class = "table-box", tableOutput("clean_table")),

        hr(class = "section-divider"),

        div(class = "card-title", style = "font-size:13px; margin-bottom:10px;", "Summary Statistics"),
        div(class = "table-box", tableOutput("stats_table"))
      )
    )
  }

  # ── File input (re-renders on reset to clear) ──────────────────────────────
  output$file_input_ui <- renderUI({
    reset_count()
    tagList(
      tags$div(
        style = "display:flex; align-items:center; width:100%;",
        tags$label(
          `for` = "csv_file_real",
          style = "background:linear-gradient(135deg,#4f7ef8,#7b5cf0); color:#fff; border-radius:8px 0 0 8px; padding:0 14px; height:38px; display:flex; align-items:center; font-size:12px; font-weight:600; cursor:pointer; white-space:nowrap; flex-shrink:0; font-family:Inter,sans-serif; margin:0;",
          "Browse"
        ),
        tags$input(
          id = "csv_file_display",
          type = "text",
          readonly = "readonly",
          placeholder = "No file chosen",
          style = "flex:1; min-width:0; height:38px; border:1.5px solid #e4e8f5; border-left:none; border-radius:0 8px 8px 0; background:#f7f8fc; color:#8a93b0; font-size:12px; font-family:Inter,sans-serif; padding:0 10px; outline:none;"
        ),
        tags$input(
          id = "csv_file_real",
          type = "file",
          accept = ".csv",
          style = "display:none;",
          onchange = "var f=this.files[0]; document.getElementById('csv_file_display').value=f?f.name:'No file chosen'; var r=new FileReader(); r.onload=function(e){Shiny.setInputValue('csv_text',e.target.result,{priority:'event'});}; r.readAsText(f);"
        )
      )
    )
  })

  # ── Column tags ────────────────────────────────────────────────────────────
  output$col_tags_ui <- renderUI({
    df <- rv_stu()
    if (nrow(df) == 0) return(NULL)
    d    <- detect_cols()
    cols <- colnames(df)
    div(class = "col-tags-row",
      lapply(cols, function(col) {
        if (is.numeric(df[[col]])) {
          tags$span(class = "col-tag", paste0("# ", col))
        } else {
          tags$span(class = "col-tag-cat", paste0("A ", col))
        }
      })
    )
  })

  # ── Data table or empty state ──────────────────────────────────────────────
  output$data_table_or_empty <- renderUI({
    df <- rv_stu()
    if (nrow(df) == 0) {
      div(class = "empty-state",
        div(class = "e-icon", "📂"),
        div(class = "e-text", "No data loaded yet"),
        div(class = "e-sub",  "Upload a CSV file or add students manually")
      )
    } else {
      div(class = "table-box", tableOutput("stu_table"))
    }
  })

  output$stu_table <- renderTable({ rv_stu() }, hover = TRUE)

  # ── Plot choices ───────────────────────────────────────────────────────────
  output$plot_choices_ui <- renderUI({
    df <- rv_stu()
    if (nrow(df) == 0)
      return(div(class = "empty-state",
        div(class = "e-icon", "📊"),
        div(class = "e-text", "No data yet"),
        div(class = "e-sub", "Go to the Data tab first")
      ))

    d       <- detect_cols()
    choices <- c()
    if (!is.na(d$name_col) && d$has_marks)
      choices["Bar Chart — Marks by Student"]          <- "bar"
    if (d$has_hours && d$has_marks)
      choices["Scatter + Line — Study Hours vs Marks"] <- "scatter"
    if (d$has_attend)
      choices["Histogram — Attendance"]                <- "hist_attend"
    if (d$has_marks)
      choices["Histogram — Marks Distribution"]        <- "hist_marks"
    if (d$has_marks)
      choices["Boxplot — Marks"]                       <- "box_marks"
    if (length(d$numeric_cols) >= 2)
      choices["Scatter — Two Numeric Columns"]         <- "scatter2"
    if (d$has_gender)
      choices["Pie Chart — Gender"]                    <- "pie_gender"
    if (d$has_parent)
      choices["Bar Chart — Parental Education"]        <- "bar_parent"

    if (length(choices) == 0)
      return(tags$p(class = "help-block", "No suitable columns detected."))

    selectInput("stu_plot_type", "Select Chart", choices = choices)
  })

  output$plot_note_ui <- renderUI({
    req(input$stu_plot_type)
    df <- rv_stu()
    if (nrow(df) == 0) return(NULL)
    d <- detect_cols()
    msg <- switch(input$stu_plot_type,
      "bar"         = paste("columns:", d$name_col, "&", d$marks_col),
      "scatter"     = paste("columns:", d$hours_col, "&", d$marks_col),
      "hist_attend" = paste("column:", d$attend_col),
      "hist_marks"  = paste("column:", d$marks_col),
      "box_marks"   = paste("column:", d$marks_col),
      "scatter2"    = paste("columns:", d$numeric_cols[1], "&", d$numeric_cols[2]),
      "pie_gender"  = paste("column:", d$gender_col),
      "bar_parent"  = paste("column:", d$parent_col),
      ""
    )
    div(class = "info-note", paste("\u26a1 Auto-detected \u2192", msg))
  })

  # ── ggplot2 theme ──────────────────────────────────────────────────────────
  theme_clean <- function() {
    theme_minimal(base_family = "sans") +
      theme(
        plot.background   = element_rect(fill = "#f7f8fc", color = NA),
        panel.background  = element_rect(fill = "#f7f8fc", color = NA),
        panel.grid.major  = element_line(color = "#e8ebf5", linewidth = 0.6),
        panel.grid.minor  = element_blank(),
        axis.text         = element_text(color = "#6b748f", size = 11),
        axis.title        = element_text(color = "#3a4060", size = 12, face = "bold"),
        plot.title        = element_text(color = "#1e2235", size = 15,
                                         face = "bold", margin = margin(b = 14)),
        legend.background = element_rect(fill = "#f7f8fc", color = NA),
        legend.text       = element_text(color = "#6b748f", size = 11),
        legend.title      = element_text(color = "#6b748f", size = 11),
        plot.margin       = margin(16, 16, 16, 16)
      )
  }

  # ── Generate plot ──────────────────────────────────────────────────────────
  output$stu_plot <- renderPlot({
    req(input$plot_stu)
    isolate({
      req(input$stu_plot_type)
      df <- rv_stu()
      validate(need(nrow(df) > 0, "No data — go to the Data tab first."))
      d  <- detect_cols()

      type <- input$stu_plot_type
      p <- ggplot(df) + theme_clean()

      if (type == "bar") {
        p <- p + aes(x = .data[[d$name_col]], y = .data[[d$marks_col]]) +
          geom_col(fill = "blue") + labs(title = "Marks of Students", x = d$name_col, y = d$marks_col)
      } else if (type == "scatter") {
        p <- p + aes(x = .data[[d$hours_col]], y = .data[[d$marks_col]]) +
          geom_point(color = "red", size = 3) + geom_line(color = "green", linewidth = 1) +
          labs(title = "Study Hours VS Marks", x = d$hours_col, y = d$marks_col)
      } else if (type == "hist_attend") {
        p <- p + aes(x = .data[[d$attend_col]]) +
          geom_histogram(binwidth = 5, fill = "orange", color = "black") +
          labs(title = "Attendance Distribution", x = d$attend_col, y = "Frequency")
      } else if (type == "hist_marks") {
        p <- p + aes(x = .data[[d$marks_col]]) +
          geom_histogram(fill = "blue", color = "white", binwidth = 5) +
          labs(title = "Distribution of Marks", x = d$marks_col, y = "Number of Students")
      } else if (type == "box_marks") {
        p <- p + aes(y = .data[[d$marks_col]]) +
          geom_boxplot(fill = "green", color = "black") + labs(title = "Boxplot of Marks", y = d$marks_col)
      } else if (type == "scatter2") {
        p <- p + aes(x = .data[[d$numeric_cols[1]]], y = .data[[d$numeric_cols[2]]]) +
          geom_point(color = "purple", size = 3) +
          labs(title = paste(d$numeric_cols[1], "vs", d$numeric_cols[2]), x = d$numeric_cols[1], y = d$numeric_cols[2])
      } else if (type == "pie_gender") {
        gd <- as.data.frame(table(df[[d$gender_col]]))
        colnames(gd) <- c("Gender", "Count")
        p <- ggplot(gd, aes(x = "", y = Count, fill = Gender)) + geom_col(width = 1, color = "white") +
          coord_polar(theta = "y") + scale_fill_manual(values = c("female" = "pink", "male" = "lightblue", "Female" = "pink", "Male" = "lightblue")) +
          labs(title = "Distribution of Gender") + theme_void() +
          theme(plot.background = element_rect(fill = "#f7f8fc", color = NA), plot.title = element_text(color = "#1e2235", size = 15, face = "bold", margin = margin(b = 14)), legend.text = element_text(color = "#6b748f"))
      } else if (type == "bar_parent") {
        pe <- as.data.frame(table(df[[d$parent_col]]))
        colnames(pe) <- c("Education", "Count")
        p <- ggplot(pe, aes(x = Education, y = Count)) + geom_col(fill = "red") +
          labs(title = "Distribution of Parental Levels of Education", x = d$parent_col, y = "Number of Students") +
          theme_clean() + theme(axis.text.x = element_text(angle = 30, hjust = 1))
      }
      p
    })
  }, bg = "#f7f8fc")

  # ── Data Cleaning ──────────────────────────────────────────────────────────

  observeEvent(input$clean_data, {
    df <- rv_stu()
    req(nrow(df) > 0)
    num_cols <- colnames(df)[sapply(df, is.numeric)]
    for (col in num_cols) {
      df[[col]][is.na(df[[col]])] <- mean(df[[col]], na.rm = TRUE)
    }
    cleaned(df)
  })

  observeEvent(input$show_stats, {
    df       <- if (!is.null(cleaned())) cleaned() else rv_stu()
    req(nrow(df) > 0)
    num_cols <- colnames(df)[sapply(df, is.numeric)]
    result   <- do.call(rbind, lapply(num_cols, function(col) {
      data.frame(
        Column        = col,
        Mean          = round(mean(df[[col]],   na.rm = TRUE), 2),
        Median        = round(median(df[[col]], na.rm = TRUE), 2),
        Std_Deviation = round(sd(df[[col]],     na.rm = TRUE), 2)
      )
    }))
    stats_data(result)
  })

  output$stats_cards_ui <- renderUI({
    df <- if (!is.null(cleaned())) cleaned() else rv_stu()
    if (nrow(df) == 0) return(NULL)
    d <- detect_cols()
    if (!d$has_marks) return(NULL)
    col <- d$marks_col
    div(class = "stat-row",
      div(class = "stat-card",
        div(class = "s-label", "Mean"),
        div(class = "s-value", round(mean(df[[col]], na.rm = TRUE), 1))
      ),
      div(class = "stat-card",
        div(class = "s-label", "Median"),
        div(class = "s-value", round(median(df[[col]], na.rm = TRUE), 1))
      ),
      div(class = "stat-card",
        div(class = "s-label", "Std Dev"),
        div(class = "s-value", round(sd(df[[col]], na.rm = TRUE), 1))
      )
    )
  })

  output$clean_table  <- renderTable({ cleaned() },    hover = TRUE)
  output$stats_table  <- renderTable({ stats_data() }, hover = TRUE)
}

shinyApp(ui = ui, server = server)
