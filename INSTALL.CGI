This simple tool is compose of 4 files

GRAPH.cgi		the perl script
graphmaker.html		the form
cgi-lib.pl		The cgi-lib.pl library has become the de facto standard
			library for creating Common Gateway Interface (CGI)
			scripts in the Perl language
separator_skip.html	a file to explain the field separator and the checkbox
			Skip blanks


1) Check if you have PERL. You can find it at http://www.perl.com

2) Control the path of your perl installation. The default in GRAPH.cgi is
   #!/usr/local/bin/perl -Tw

3) Check if you have GD.pm (A graphics library for fast GIF creation in perl).
   You can find it at http://www-genome.wi.mit.edu/ftp/pub/software/WWW/GD.html

4) Move GRAPH.cgi in /cgi-bin/ directory of your Web
   [Usually default is /usr/local/etc/httpd/cgi-bin]
   you have to modify the variables
   $Graph = "/usr/local/etc/httpd/htdocs/test/GRAPH.gif"; and the relative link
   print "<img src=\"/test/GRAPH.gif\"><p>\n";

5) Move cgi-lib.pl in the default directory of lib PERL
   [Usually /usr/local/lib/perl5]
   You can find the last version of cgi-lib.pl and documentation at
   http://www.bio.cam.ac.uk/cgi-lib/
   If you have CGI.pm installed you can you it. You have to comment in GRAPH.cgi
   the line
   require "cgi-lib.pl";
   and decomment the line
   #use CGI qw(:cgi-lib);
   You can find the last version of CGI.pm and documentation at
   http://www-genome.wi.mit.edu/ftp/pub/software/WWW/
