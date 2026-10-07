#! /usr/local/bin/perl
#
# フォームメール WebFORM v1.1 is Free. (c)rescue@ask.or.jp
#

require './jcode.pl';

#---初期設定-------------------------------------------------------------------#

#受け取り人のメールアドレス（あなたのメールアドレス）
$mailto = 'user@xxx.or.jp';

#送信後に表示するページのＵＲＬ
$location = 'http://www.xxx.or.jp/~user/mail/thanks.html';

#受け取るメールのタイトル
$subject = 'フォームメール';

#sendmailのパス（わからないときはプロバイダに聞く事）
$sendmail = '/usr/lib/sendmail';

#------------------------------------------------------------------------------#

# 時刻取得
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$month = ($mon + 1);
$date_now = "$year/$month/$mday $hour:$min:$sec";

# フォーム内容を取得
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

if ($buffer eq "") { &send_error; }

# フォーム内容を分析
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name, $value) = split(/=/, $pair);
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	if (!($value =~ /\n/) && $value =~ /\r/) { $value =~ s/\r/\n/g; }

	if ($name eq "no_check" && $value eq "on") { $nocheck = "on"; }
	else {

		if ($name eq "email") { $email = $value; }

		&jcode'convert(*name,'jis');    &jcode'convert(*value,'jis');
		push(@DATA_N,$name);            push(@DATA_V,$value);

		&jcode'convert(*name,'sjis');   &jcode'convert(*value,'sjis');
		$name =~ s/</&lt;/g;            $value =~ s/</&lt;/g;
		$name =~ s/>/&gt;/g;            $value =~ s/>/&gt;/g;
		$name =~ s/"/&quot;/g;          $value =~ s/"/&quot;/g;
		push(@DATA_NS,$name);           push(@DATA_VS,$value);
	}
}

if (!($email =~ /(.*)\@(.*)\.(.*)/)) { $email = 'nobody@xxx.xxx'; }
&jcode'convert(*subject,'jis');
$count = @DATA_NS;

if ($nocheck eq "on") { &sendmail; }

print 'Content-type: text/html' ."\n\n";
print '<html><head><title>WebFORM</title></head>' ."\n";
print '<body><h1>内容確認</h1>' ."\n";
print '<form method="post" action="webform.cgi">' ."\n";
print '<table border width=80%><tr>' ."\n";
print '<td>項目</td>' ."\n";
print '<td>内容</td></tr>' ."\n";

foreach (0..$count-1) {

	print "<input type=hidden name=\"$DATA_NS[($_)]\" value=\"$DATA_VS[($_)]\">\n";
	print '<tr>' ."\n";
	print "<td>$DATA_NS[($_)]</td>\n";
	chop($DATA_VS[($_)]) if $DATA_VS[($_)] =~ /\n$/;
	print "<td><pre>$DATA_VS[($_)]<pre></td>\n";
	print '<tr>' ."\n";
}

print '</tr></table><p>' ."\n";
print '<input type=hidden name="no_check" value="on">' ."\n";
print '<input type=submit value="確認"><p>' ."\n";
print '</form>' ."\n";
print "<hr><i>送信先：<a href=\"mailto:$mailto\">$mailto</a><i>\n";
print '<p></body></html>' ."\n";
exit;

sub sendmail {

	if (!open(OUT,"| $sendmail $mailto")) { &send_error; }

	print OUT 'X-Mailer: WebFORM v1.1 (c)rescue@ask.or.jp' ."\n";
	print OUT "To: $mailto\n";
	print OUT "From: $email\n";
	print OUT "Subject: $subject\n";
	print OUT "Content-Transfer-Encoding: 7bit\n";
	print OUT "Content-Type: text/plain\n";
	print OUT "\n\n";

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	print OUT "DATE            : $date_now\n";
	print OUT "REMOTE_HOST     : $host\n";
	print OUT "REMOTE_ADDR     : $addr\n";
	print OUT "HTTP_USER_AGENT : $ENV{'HTTP_USER_AGENT'}\n";
	print OUT "----------------------------------------------------\n\n";

	foreach (0..$count-1) {	print OUT "$DATA_N[($_)] = $DATA_V[($_)]\n"; }

	print OUT "\n";
	print OUT "----------------------------------------------------\n";
	close(OUT);

	print "Location: $location\n\n";
	exit;
}

sub send_error {

	print 'Content-type: text/html' ."\n\n";
	print '<html><head><title>WebFORM</title></head>' ."\n";
	print '<body>' ."\n";
	print '<H2>何らかの原因で送信できませんでした</H2>' ."\n";
	print '</body></html>' ."\n";
	exit;
}
