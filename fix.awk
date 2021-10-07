#!/opt/local/bin/gawk -f
BEGIN {
   print "% Fixed by fix.awk " strftime("%F %T")
   announcements_block_fixed=0
   # to set the date on the command line, use:
   # $ fix.awk -v docdate="YYYY MM DD HH MM SS" ...
   # Otherwise the current date/time is used.
   if (!docdate) {
       docdate_ts=systime()
   } else {
       docdate_ts=mktime(docdate)
   }
   docdate_en = strftime("%B %e, %Y",docdate_ts)
   docdate_iso = strftime("%F",docdate_ts)
}

# fix date
/^\\date/ {
    print "\\date{" docdate_en "}"
    next
}
# fix course section
# FIXME: course may not be on a single line.
/^\\course/ {
    print "\\course[code=MATH-UA 123,section=007]{Calculus III}"
    next
}
# fix term
/^\\term/ {
    print "\\term[code=2015F]{Fall 2015}"
    next
}
/\\DTLloaddb/ {
    announcements_block_fixed=1
}

# add before \begin{document}
/\\begin{document}/{
    if (announcements_block_fixed=0) {
        print "\\usepackage{datatool}"
        print "\\DTLloaddb{announcements}{../announcements.csv}"
        print "\\dtlsort{endDate}{announcements}{\\dtlcompare}"
        print "\\begin{document}"
        next
    }
}

## need to replace
# \section*{Announcements}
# \timecheck{\LARGE\clock{8}{55}}
# \gdef\announcements{
# Welcome to the course!  The syllabus is on NYUClasses.  Read it.
# \begin{itemize}
# \item WebAssign for \S6.6 due Friday/Saturday 5PM
# \item Written HW due Monday/Tuesday
# \item Quiz 2 on \S\S 6.4--6.6 is February 27/28
# \end{itemize}}
# \begin{block}{Announcements}
# \announcements
# \end{block}
# # with
# \maketitle
# 
# \section*{Announcements}
# \timecheck{\LARGE\clock{11}{00}}
# \begin{itemize}
# \DTLforeach{announcements}{\annText=announcementText}{\item \annText}
# \end{itemize}
/\\section\*{Announcements}/,/\\end{block}/ {
    if (announcements_block_fixed == 0 ) {
        print "\\section*{Announcements}"
        print "\\timecheck{\\LARGE\\clock{2}{00}}"
        print "\\begin{itemize}"
        print "\\DTLforeach[\\DTLisgt{\\endDate}{" docdate_iso "}\\and\\not\\DTLisgt{\\startDate}{" docdate_iso "}]{announcements}{\\annText=announcementText,\\endDate=endDate,\\startDate=startDate}{\\item \\annText}"
        print "\\end{itemize}"
        announcements_block_fixed=1
    }
    next
}
/NYUMathematics/ {
    sub(/NYUMathematics/,"NYUCourant")
    print
    next
}

# default: just print
{
    print 
}

