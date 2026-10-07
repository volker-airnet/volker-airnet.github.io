#!/usr/local/bin/perl
#
#   YY-BOARD v4.54 (2001/09/06) copyright(C)
$ver = 'YYBBS v4.54 & YYBBS-P v4.63';
#   改造版 YYBBS-P v4.63 (2003/03/10) copyright(C)
# ■作成者 KENT
#  webmaster@kent-web.com
#  http://www.kent-web.com/
# ■改造配布者 satoko
#  satoko@pop.hotcake.ne.jp
#  http://www60.tok2.com/home/september/index.shtml
# ■注意事項
#  1,このスクリプトはフリーソフトです。このスクリプトを使用した
#    いかなる損害に対して作者、改造者共に、一切の責任を負いません。
#  2,設置に関する質問は、改造者にメールか掲示板でお願いします。
#  3,改造は可ですが、改造の有無にかかわらず、再配布は不可です。
#  4,著作権表示や出所URLの表示などは変更しないでください。
# ■その他、参考にさせていただいたスクリプト
#   Force 264 BBS  (by carl http://www3.digitalworkz.com/~carl/)
#   投稿コード掲示板  (by mm http://www2s.biglobe.ne.jp/~cru/)
# ■設置例
# カッコの中が最も甘く、カッコの右側が最も厳しい所有者権限のアクセス権です。
# ご自分のサーバーに合わせて、できるだけ厳しくしてください。
#  public_html (ホームディレクトリ)
#      |
#      +-- yybbs [777]701
#            |   / yybbs.cgi  [755]700
#            |     yybbs.log  [666]600★必ずファイル名変更すること
#            |     count.dat  [666]600
#            |     jcode.pl   [644]600
#            |     pastno.dat [666]600
#            |     log.txt    [666]604★必ずファイル名変更すること
#            |     index.html [666]604★白紙のダミーファイル
#            +-- img  [777]701 / home.gif, bear.gif, ...
#            |
#            +-- lock [777]701 /
#            |
#            +-- past [777]701/ 1.dat [666]600 ...
#
#============#
#  設定項目  #
#============#
# ★★改造、追加した機能は、★マークをつけています★★
# 文字コードライブラリ取込
require './jcode.pl';

# タイトル名を指定
$title = "フォルカーの部屋 - 芳名録 -";

# タイトルの大きさ（ポイント数:スタイルシートで有効）
$t_size = '18pt';

# タイトル文字のフォントタイプ
$t_face = "ＭＳ Ｐゴシック";

# 本文の文字大きさ（ポイント数:スタイルシートで有効）
$b_size = '10pt';

# 壁紙を指定する場合（http://から指定）
$backgif = "";

# リンク色を指定
$link  = "#0000FF";	# 未訪問
$vlink = "#800080";	# 訪問済
$alink = "#FF0000";	# 訪問中

# 戻り先のURL (index.htmlなど)
$homepage = "../index.html";

# 最大記事数
$max = 100;

# 管理者用マスタパスワード (英数字で８文字以内)
$pass = '1409';

# ★会員パスワードを(1=使用,0=使用しない)
$use_passwd= 0;
	
# 会員パスワードを設定する（★必ず管理人用、削除用とは別のものにしてください）
$member_passwd='abcd';

# アイコン画像のある「ディレクトリ」
# → フルパスなら http:// から記述する
# → 最後は必ず / で閉じる
$imgurl = "./img/";

# アイコンを定義（上下は必ずペアで）
@icon1 = ('bear.gif','cat.gif','cow.gif','dog.gif','fox.gif','hituji.gif',
		'monkey.gif','zou.gif','mouse.gif','panda.gif','pig.gif','usagi.gif');
@icon2 = ('くま','ねこ','うし','いぬ','きつね','ひつじ',
		'さる','ぞう','ねずみ','パンダ','ぶた','うさぎ');

# 管理者専用アイコン機能 (0=no 1=yes)
# → 【使い方】記事投稿時に「管理者アイコン」を選択し、パスワードに
#             「管理用パスワード」を入力して下さい。
$my_icon = 0;

# 管理者専用アイコンの「ファイル名」を指定
$my_gif  = 'admin.gif';

# アイコンモード (0=no 1=yes)
$icon_mode = 0;

# 返信がつくと親記事をトップへ移動 (0=no 1=yes)
$topsort = 1;

# タイトルにGIF画像を使用する時 (http://から記述)
$title_gif = "houmei2.gif";
$tg_w = '227';	# GIF画像の幅 (ピクセル)
$tg_h = '43';	#    〃    高さ (ピクセル)

# ファイルロック形式
# → 0=no 1=symlink関数 2=mkdir関数
$lockkey = 0;

# ロックファイル名
$lockfile = './lock/yybbs.lock';

# ミニカウンタの設置
# → 0=no 1=テキスト 2=GIF画像
$counter = 1;

# ミニカウンタの桁数
$mini_fig = 6;

# テキストのとき：ミニカウンタの色
$cnt_color = "#DD0000";

# ＧＩＦのとき：画像までのディレクトリ
# → 最後は必ず / で閉じる
$gif_path = "./img/";
$mini_w = 8;		# 画像の横サイズ
$mini_h = 12;		# 画像の縦サイズ

# カウンタファイル
$cntfile = './count.dat';

# タグの許可 (0=no 1=yes)★許可すると危険です
$tagkey = 0;

# スクリプトのファイル名
# → フルパスで指定する場合は http:// から記述
$script  = './volkerbbs.cgi';

# ログファイルを指定★ファイル名は必ず変更してください★
# → フルパスで指定する場合は / から記述
$logfile = './volkerbbsnew.log';

# メールアドレスの入力必須 (0=no 1=yes)
$in_email = 0;

# 記事 [タイトル] 部の長さ (全角文字換算)
$sub_len = '30';

# 背景色を指定
$bgcolor = "#E1F0F0";

# タイトルの色
$t_color = "#0000cc";

# 文字色を指定
$text = "#000000";

# 記事の [タイトル] 部の文字色
$sub_color = "#0000cc";

# ★記事表示部の下地の色
$tbl_color = "#ffffff";

# ★モードタイトルバーの色
$tbl_color3 = "#0000cc";

# ★投稿者のリモートホスト表示（0=no 1=yes）
$d_host = 1;

# ★ユーザーエージェント表示（0=no 1=yes）
$dp_agent= 1;

# ★リモートホスト、ユーザーエージェント表示の際のカラー設定
$host_color = '#808080';

# ★プロクシ経由でのアクセス（閲覧）＆書き込みの許可（by カール＆dimdim氏＆ひみこ氏）
# 許可する : 0　書き込みのみ拒否する（閲覧は可）: 1　閲覧、書き込み共に拒否: 2
# YahooBBはアクセス制限を回避しましたので、制限する場合は、275行目で設定してください。
$proxy = 0;

# ★プロクシ制限する場合のレベル（弱 : 1　強 : 2）
# ２にするとプロクシ変数をまったく吐かないＪＰ串以外はほとんど拒否します。
$plevel = 2;

# ★上記プロクシ制限をした場合に善意のアクセス者（会社のFireWall等）を指定して許可する設定
# ホスト名を|で区切って複数指定可能。IPアドレスの場合は先頭の２つが適当？
# 設定例：$kyoka = "biglobe.be.jp|3web.ne.jp|202.124.|abc.com";
$kyoka = "";

# ★アクセスログを記録するかどうか（記録しない: 0 記録する : 1）
# アクセスログを使う場合の記録ファイルの設定 
# ★必ずファイル名を変更すること★初期値のままだとパスワードがばれてしまいます。
$alog = 1;
$access_log = "./volkerlog.txt";

# アクセスログ最大記録件数（設定数以上は古いものから順に削除）
$rescue = '300';

# 家アイコンの使用 (0=no 1=yes)
$home_icon = 0;
$home_gif = "home.gif";	# 家アイコンのファイル名
$home_wid = 16;		# 画像の横サイズ
$home_hei = 20;		#   〃  縦サイズ

# イメージ参照画面の表示形態
#  1 : JavaScript
#  2 : HTML (JavaScriptが不安定なブラザが多い場合はこちら）
$ImageView = 2;

# イメージ参照画面のサイズ (JavaScriptの場合)
$img_w = '550'; # 横幅
$img_h = '450'; # 高さ

# 同一IPアドレスからの連続投稿時間（秒数）
# → 連続投稿などの荒らし対策
# → 値を 0 にするとこの機能は無効になります
$wait = 600;

# １ページ当たりの記事表示数 (親記事)
$p_log = 20;

# 投稿があるとメール通知する (sendmail必須)
#  0 : 通知しない
#  1 : 通知するが、自分の投稿記事はメールしない。
#  2 : 通知する。自分の投稿記事も通知する。
$mailing = 2;

# ★書き込み通知先メールアドレス
# 携帯などに通知したいときに設定してください。必要ないときは、書き込み時と同じメールアドレスにしてください。
$mailto = 'naoya@sf.airnet.ne.jp';

# ★管理人書き込み時のメールアドレス
$mailto2 = 'naoya@sf.airnet.ne.jp';

# sendmailパス（メール通知する時）
$sendmail = '/usr/sbin/sendmail';

# ★閲覧時、参照元のチェック（0=no 1=エラーメッセージを出す 2=指定URLに飛ばす）
$ref_chk = 0;
# ★書き込み時、参照元のチェック（0=no 1=yes）
# セキュリティソフトの設定により参照元を送らない場合もあるので注意!!
$ref_chk2 = 0;
# このスクリプトの参照元URL
$chk_url = "http://";
# このスクリプトを設置したURL
$cgi_url= "http://";
# 指定URLに飛ばす場合のアドレス（初期値は警察庁、あなたのサイトのトップページでもいいかも？）
$jump_url= "http://www.npa.go.jp/";

# ★訪問者が文字色を選択できる(0=no 1=yes)
$color_s = 1;

# 文字色の設定。
@COLORS = ('#800000','#DF0000','#008040','#0000FF','#C100C1','#FF80C0','#FF8040','#000080');

# 投稿フォーム改行形式 (soft=手動 hard=強制)
$wrap = 'soft';

# URLの自動リンク (0=no 1=yes)
#  --> タグ許可の場合は no とすること。
$autolink = 1;

# タグ広告挿入オプション (FreeWebなど）
#   → <!-- 上部 --> <!-- 下部 --> の代わりに「広告タグ」を挿入する。
#   → 広告タグ以外に、MIDIタグ や LimeCounter等のタグにも使用可能です。
$banner1 = '<!-- 上部 -->';	# 掲示板上部に挿入
$banner2 = '<!-- 下部 -->';	# 掲示板下部に挿入

# アクセス制限（★ホスト名、IP名、どちらでも可。ダイヤルアップの場合は、接続のたびに変化しない部分だけを記述する。追加可能）
@deny = (
	"anonymizer",
	"207-226-171-34.pccwglobal.net",
	"ip68-109-74-164.oc.oc.cox.net",
	"249.laws.ms",
	"61.135.131.124",
	"adsl-west-3633.enjoy.ne.jp",
	"59.93.219.90",
	"62.231.243.136",
	"89-149-244-45.internetserviceteam.com",
	"qwerty.ru",
	"89-28-3-241.starnet.md",
	"zuper.ru",
	"starnet.md",
	"bristol.sweb.ru",
	"ukservers.com",
	"195.2.253.86",
	"unknown.steephost.net",
	"210.51.54.165",
	);

# ★ストップモード(0=no 1=yes)
$stopmode = 0;

# ★ストップメッセージ
$StopMsg = <<'STOPMSG';
申し訳ありませんが、管理人が旅行中のため、
しばらく投稿を中止します。
STOPMSG

#---(以下は「過去ログ」機能を使用する場合の設定です)---#
#
# 過去ログ生成 (0=no 1=yes)
$pastkey = 1;

# 過去ログ用NOファイル
$nofile  = './pastno.dat';

# 過去ログのディレクトリ
# → フルパスなら / から記述（http://からではない）
# → 最後は必ず / で閉じる
$pastdir = './past/';

# 過去ログ１ファイルの行数
# → この行数を超えると次ページを自動生成します
$log_line = '600';

#============#
#  設定完了  #
#============#
# メイン処理
&decode;
&axs_check;
if ($mode eq "howto") { &howto; }
elsif ($mode eq "find") { &find; }
elsif ($mode eq "usr_del") { &usr_del; }
elsif ($mode eq "usr_edt") { &usr_edt; }
elsif ($mode eq "regist") { &regist; }
elsif ($mode eq "res") { &res_form; }
elsif ($mode eq "admin") { &admin; }
elsif ($mode eq "image") { &image; }
elsif ($mode eq "past") { &past; }
elsif ($mode eq "check") { &check; }
&html_log;

#----------------#
#  アクセス制限  #
#----------------#
sub axs_check {
	# ホスト名を取得
	&get_host;

	# 時間を取得
	&get_time;

	# ログを取らず、Proxyチェックもしない場合は負荷軽減のため下記変数を取得しない処理
	# ただし、その場合でも投稿時には必要なためフラッグを立ててregistルーチンで取得
	if ($alog == 1 || $proxy != 0) {
	$via    = $ENV{'HTTP_VIA'};
	$xfor   = $ENV{'HTTP_X_FORWARDED_FOR'};
  	$for    = $ENV{'HTTP_FORWARDED'};
  	$agent  = $ENV{'HTTP_USER_AGENT'};
  	$trueip = &getip;
  	$pcheck_flag = 1;
	}

	# ★アクセスログを取る場合の処理
	if ($alog) {
    	&acount; }
	
	# Proxy経由の閲覧禁止の場合はProxyチェックへ。ただし書き込みのみ禁止の場合はここはスルー
	if ( ($kyoka eq "") && ($proxy == 2) ) {
  	&proxy;
	} elsif ( ($host !~ /$kyoka/) && ($proxy == 2) ) {
  	&proxy;
	}
	
	# ホスト名チェック
	local($flag)=0;
	foreach (@deny) {
		if (!$_) { next; }
		$_ =~ s/\*/\.\*/g;
		if ($host =~ /$_/i || $addr =~ /$_/) { $flag=1; last; }
	}
	if ($flag) { &error("アクセスを許可されていません"); }
	
	# ★参照元のチェック
	if ($ref_chk == 1 ){
		if(($ENV{'HTTP_REFERER'} !~ $cgi_url) && ($ENV{'HTTP_REFERER'} !~ $chk_url)){
		&error("参照元が不正です。トップページからどうぞ");
		}
	}
	elsif ($ref_chk == 2){
		if(($ENV{'HTTP_REFERER'} !~ $cgi_url) && ($ENV{'HTTP_REFERER'} !~ $chk_url)){
		print "Content-type: text/html\n";
  		print "Location: $jump_url\n\n";
  		exit;
		}
	}
}

#--------------#
#  記事表示部  #
#--------------#
sub html_log {
	local($no,$reno,$date,$name,$mail,
		$sub,$comment,$url,$host,$pw,$color,$icon,$p_flag,$agent);

	# クッキーを取得
	&get_cookie;

	# フォーム長を調整
	&get_agent;

	# ヘッダを出力
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# ★stopmode時のメッセージ
	if ($stopmode==1){
		  $FORM{'MSGBODY'}=$StopMsg;
	}

	# カウンタ処理
	if ($counter) { &counter; }

	# タイトル部
	print "<center>\n";
	if ($banner1 ne "<!-- 上部 -->") { print "$banner1<P>\n"; }
	if ($title_gif eq '') {
		print "<font color=\"$t_color\" size=6 face=\"$t_face\"><b><span>$title</span></b></font>\n";
	} else {
		print "<img src=\"$title_gif\" width=\"$tg_w\" height=\"$tg_h\" alt=\"$title\">\n";
	}

	print "<hr width='90%'>\n";
	print "[<a href=\"$homepage\" target='_top'>Home</a>]\n";
	print "[<a href=\"$script?mode=howto\">HowTo</a>]\n";
	print "[<a href=\"$script?mode=find\">Search</a>]\n";

	# 過去ログのリンク部を表示
	if ($pastkey) {	print "[<a href=\"$script?mode=past\">Log</a>]\n"; }
	print <<"EOM";
[<a href="$script?mode=admin">Master</a>]
<hr width='90%'>
</center>
<form method=POST action="$script">
<input type=hidden name=mode value="regist"><center>
EOM
	&kakikomi;
	
	print "</center></form>\n";
	print "<center><br>\n";
		
	# ページ区切り処理
	$start = $page + 1;
	$end   = $page + $p_log;

	# 記事を展開
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	$i=0;
	$flag=0;
	while (<IN>) {
		($no,$reno,$date,$name,$mail,$sub,
			$comment,$url,$host,$pw,$color,$icon,$agent) = split(/<>/);

		if ($reno eq "") { $i++; }
		if ($i < $start) { next; }
		if ($i > $end) { next; }

		# Titleの長さ
		if (length($sub) > $sub_len*2) {
			$sub = substr($sub,0,$sub_len*2);
			$sub .= "...";
		}

		if ($mail) { $name = "<a href=\"mailto:$mail\">$name</a>"; }
		if ($home_icon && $url) { $url = "<a href=\"http://$url\" target='_blank'><img src=\"$imgurl$home_gif\" border=0 align=top alt='HomePage' width=\"$home_wid\" height=\"$home_hei\"></a>"; }
		elsif (!$home_icon && $url) { $url = "&lt;<a href=\"http://$url\" target='_blank'>HOME</a>&gt;"; }
		if (!$icon_mode) { $comment = "<blockquote>$comment</blockquote>"; }

		if (!$reno && $flag) {
			print "</td></tr></table><br><br>\n";
			$flag=1;
		}
		if (!$reno) {
			print "<table border=1 width='90%' bgcolor=\"$tbl_color\" cellspacing=0 cellpadding=2><tr><td>\n";
			$flag=1;
		}

		if ($reno) { print "<hr noshade size=1 width='85%'>\n"; }
		print "<table border=0 cellpadding=2><tr>\n";
		if ($reno) { print "<td rowspan=2 width=40><br></td>"; }

		print "<td valign=top nowrap><font color=\"$sub_color\"><b>$sub</b></font>　";

		if (!$reno) { print "Name：<b>$name</b> <small>Date：$date</small> "; }
		else { print "<b>$name</b> - <small>$date</small> "; }

		print "<font color=\"$sub_color\"><small>No\.$no</small></font></td>";
		print "<td valign=top nowrap> &nbsp; $url </td><td valign=top>\n";

		if (!$reno) {
			print "<form action=\"$script\" method=POST>\n";
			print "<input type=hidden name=mode value=res>\n";
			print "<input type=hidden name=no value=$no>\n";
			print "<input type=submit value='Res'></td></form>\n";
		} else {
			print "<br></td>\n";
		}

		print "</tr></table><table width=90% border=0 cellpadding=5><tr>\n";
		if ($reno) { print "<td width=32><br></td>\n"; }

		# アイコンモード
		if ($icon_mode && $icon ne "") { print "<td><img src=\"$imgurl$icon\" alt=\"$icon\"></td>"; }

		print "<td><font color=\"$color\">$comment</font>\n";

		# ★リモートホスト・ユーザーエージェント表示
		if($d_host == 1 || $dp_agent == 1) {
		print "<p align=right>\n";
		}
                if ($d_host==1){
		print"<font color=$host_color size=-1>【$host】</font>\n";
		}
                if ($dp_agent ==1){
                print"<font color=\"$host_color\" size=-1>$agent</font>\n";
                }
        print "</td></tr></table>\n";

	}
	close(IN);
	print "</td></tr></table></center>\n";

	$next_page = $page + $p_log;
	$back_page = $page - $p_log;

	$p_flag=0;
	print "<P><blockquote><table cellpadding=0 cellspacing=0><tr>\n";
	if ($back_page >= 0) {
		$p_flag=1;
		print "<td><form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=page value=\"$back_page\">\n";
		print "<input type=submit value=\"Back\">\n";
		print "</td></form>\n";
	}
	if ($next_page < $i) {
		$p_flag=1;
		print "<td><form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=page value=\"$next_page\">\n";
		print "<input type=submit value=\"Next\">\n";
		print "</td></form>\n";
	}

	# ページ移動ボタン表示
	if ($p_flag) {
		print "<td width=10></td><td>[Jump]\n";
		$x=1;
		$y=0;
		while ($i > 0) {
			if ($page == $y) { print "[<b>$x</b>]\n"; }
			else { print "[<a href=\"$script?page=$y\">$x</a>]\n"; }
			$x++;
			$y = $y + $p_log;
			$i = $i - $p_log;
		}
		print "</td>\n";
	}
	print "</tr></table></blockquote>\n<div align=center>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<font color=$t_color><small>- Edit ＆ Delete Form -</small></font><br>\n";
	print "Select <select name=mode>\n";
	print "<option value=usr_edt>Edit\n";
	print "<option value=usr_del>Delete</select>\n";
	print "No <input type=text name=no size=3>\n";
	print "DeletePass <input type=password name=pwd size=4 maxlength=8>\n";
	print "<input type=submit value=\"Submit\"></form>\n";

	# 著作権表示部
	# MakiMakiさんの画像使用の有無に関わらずこの2箇所のリンク部の
	# 削除改変を禁止します
	print "$banner2<P><small><!-- $ver -->\n";
	print "<div align=right><a href='http://www.kent-web.com/' target='_blank'>KENT</a> &amp; ";
	print "<a href='http://village.infoweb.ne.jp/~fwhf2602/' target='_blank'>MakiMaki</a>\n";
	print "<br>Edit by <a href='http://www60.tok2.com/home/september/index.shtml' target='_blank'>satoko</a>\n";
	print "</small></div>\n</body>\n</html>\n";
	exit;
}

#----------------#
#  ログ書込処理  #
#----------------#
sub regist {
	local(@lines,@new,@tmp,$top,$no,$ip,$time2,$no2,$reno2,
		$date2,$name2,$mail2,$sub2,$com2,$flag,$ango,$stop,$match,$agent2);

        # ★ストップモード
        if ($stopmode==1){
		&error( "$StopMsg");
	}

        # ★会員パスワードチェック
        if ($use_passwd==1){
        	 if ($in{'entry_passwd'} ne "$member_passwd"){&error(" MemberPassが違います。投稿できませんでした。"); }
        }
        
	# ★変数の取得とプロクシチェック（アクセス時にログを取っていなかった場合）
  	if ($pcheck_flag != 1) {
    	$via    = $ENV{'HTTP_VIA'};
    	$xfor   = $ENV{'HTTP_X_FORWARDED_FOR'};
    	$for    = $ENV{'HTTP_FORWARDED'};
    	$agent  = $ENV{'HTTP_USER_AGENT'};
    	$trueip = &getip;
  	}
  	if ( ($kyoka eq "") && ($proxy == 1) ) {
    	&proxy;
  	} elsif ( ($host !~ /$kyoka/) && ($proxy == 1) ) {
    	&proxy;
  	}

	# フォーム入力チェック
	&form_check;

	# クッキーを発行
	&set_cookie;

	# ファイルロック
	if ($lockkey) { &lock; }

	# ログを開く
	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);

	# 記事NO処理
	$top = shift(@lines);
	($no,$ip,$time2) = split(/<>/, $top);
	$no++;

	# 連続投稿チェック
	#if ($addr eq $ip && $wait > $times - $time2)
	#		{ &error("連続投稿はもうしばらく時間をおいて下さい"); }

	# URL自動リンク
	if ($autolink) { &auto_link($in{'comment'}); }

	# 重複チェック
	$flag=0;
	foreach (@lines) {
		($no2,$reno2,$date2,$name2,$mail2,$sub2,$com2) = split(/<>/);

		if ($in{'name'} eq $name2 && $in{'comment'} eq $com2) {
			$flag=1; last;
		}
	}
	if ($flag) { &error("重複投稿のため処理を中断しました"); }

	# パスワードを暗号化
	if ($in{'pwd'} ne "") { $ango = &encrypt($in{'pwd'}); }

	# 親記事の場合
	if ($in{'reno'} eq "") {

		$i=0;
		$stop=0;
		foreach (@lines) {
			($no2,$reno2) = split(/<>/);
			$i++;
			if ($i > $max-1 && $reno2 eq "") { $stop=1; }
			if (!$stop) { push(@new,$_); }
			elsif ($stop && $pastkey) { push(@data,$_); }
		}
		unshift(@new,"$no<><>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$in{'icon'}<>$agent<>\n");
		unshift(@new,"$no<>$addr<>$times<>\n");

		# 過去ログ更新
		if ($data[0]) { &pastlog; }

		# 更新
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);
	}
	# レス記事の場合：トップソートあり
	elsif ($in{'reno'} && $topsort) {

		$match=0;
		@new=();
		@tmp=();
		foreach (@lines) {
			($no2,$reno2) = split(/<>/);

			if ($in{'reno'} eq "$no2") {
				$match=1;
				push(@new,$_);
			}
			elsif ($in{'reno'} eq "$reno2") {
				push(@new,$_);
			}
			elsif ($match == 1 && $in{'reno'} ne "$reno2") {
				$match=2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$in{'icon'}<>$agent<>\n");
				push(@tmp,$_);
			}
			else { push(@tmp,$_); }
		}

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$in{'icon'}<>$agent<>\n");
		}
		push(@new,@tmp);

		# 更新
		unshift(@new,"$no<>$addr<>$times<>\n");
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);

	}
	# レス記事の場合：トップソートなし
	else {
		$match=0;
		@new=();
		foreach (@lines) {
			($no2,$reno2) = split(/<>/);

			if ($match == 0 && $in{'reno'} eq "$no2") { $match=1; }
			elsif ($match == 1 && $in{'reno'} ne "$reno2") {
				$match=2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$in{'icon'}<>$agent<>\n");
			}
			push(@new,$_);
		}

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$in{'icon'}<>$agent<>\n");
		}

		# 更新
		unshift(@new,"$no<>$addr<>$times<>\n");
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);
	}

	# ロック解除
	if ($lockkey) { &unlock; }

	# メール処理
	if ($mailing == 1 && $in{'email'} ne $mailto2) { &mail_to; }
	elsif ($mailing == 2) { &mail_to; }
}

#------------------# 
# 書き込みフォーム #
#------------------#
sub kakikomi{
	print "<table border=0 cellspacing=0>\n";
        if ($use_passwd == 1 && $mode ne "usr_edt"){
        	print "<tr><td nowrap><b>MemberPass</b></td>\n";
        	print "<td><input type=password name=entry_passwd size=8 maxlength=8 value=$c_entry_passwd></td></tr>\n";
	}
	print <<"EON";
<tr>
  <td nowrap><b>Name</b></td>
  <td><input type=text name=name size="$nam_wid" value="$c_name"></td>
</tr>
<tr>
  <td nowrap><b>Mail</b></td>
  <td><input type=text name=email size="$nam_wid" value="$c_email"></td>
</tr>
<tr>
  <td nowrap><b>Title</b></td>
  <td nowrap>
    <input type=text name=sub size="$sub_wid" value="$resub">
  </td>
</tr>
<tr>
  <td colspan=2>
    <b>Message</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap">$FORM{'MSGBODY'}</textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>URL</b></td>
  <td><input type=text size="$url_wid" name=url value="http://$c_url"></td>
</tr>
EON

	# 管理者アイコンを配列に付加
	if ($my_icon) {
		push(@icon1,"$my_gif");
		push(@icon2,"管理者用");
	}
	if ($icon_mode) {
		print "<tr><td nowrap><b>YourImage</b></td><td><select name=icon>\n";
		foreach(0 .. $#icon1) {
			if ($c_icon eq "$icon1[$_]") {
				print "<option value=\"$icon1[$_]\" selected>$icon2[$_]\n";			   } else {
				print "<option value=\"$icon1[$_]\">$icon2[$_]\n";
			}
		}
		print "</select> <small>(あなたのイメージを選択して下さい)</small>\n";

		# イメージ参照のリンク
		if ($ImageView == 1) {
			print "[<a href=\"javascript:ImageUp()\">画像イメージ参照</a>]";
		} else {
			print "[<a href=\"$script?mode=image\" target=\"_blank\">画像イメージ参照</a>]";
		}
		print "</td></tr>\n";
	}
	if ($mode ne "usr_edt") { 
	print "<tr><td nowrap><b>DeletePass</b></td>\n";
	print "<td><input type=password name=pwd size=8 maxlength=8 value=\"$c_pwd\">\n";
	print "<small>(記事のメンテ時に使用。英数字で8文字以内)</small></td></tr>\n";
	}
	
	# 文字色選択
	if ($color_s == 1){
	print "<tr><td nowrap><b>FontColor</b></td><td>\n";

	# クッキーの色情報がない場合
	if ($c_color eq "") { $c_color = $COLORS[0]; }

	foreach (0 .. $#COLORS) {
		if ($c_color eq "$COLORS[$_]") {
			print "<input type=radio name=color value=\"$COLORS[$_]\" checked>";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$COLORS[$_]\">";
			print "<font color=\"$COLORS[$_]\">■</font>\n";
		}
	}
	}
        print "<tr><td colspan=\"2\"><input type=submit value=\"Submit\">　<input type=reset value=\"Reset\"></td></tr>\n";
	print "</td></tr></table>\n";
}
#----------------#
#  返信フォーム  #
#----------------#
sub res_form {
	local($no,$reno,$date,$name,$mail,$sub,$com,$url,$resub);

	# フォーム長を定義
	&get_agent;

	# クッキーを取得
	&get_cookie;

	# ログを読み込み
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;

	# ヘッダを出力
	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }

	# ★stopmode時のメッセージ
	if ($stopmode==1){
		  $FORM{'MSGBODY'}=$StopMsg;
	}	

	# 関連記事出力
	print "- 以下は、記事NO. <B>$in{'no'}</B> に関する<a href='#RES'>返信フォーム</a>です -<hr>\n";

	while (<IN>) {
		($no,$reno,$date,$name,$mail,$sub,$com,$url) = split(/<>/);

		if ($in{'no'} == $no || $in{'no'} == $reno) {

			if (length($sub) > $sub_len*2) {
				$sub = substr($sub,0,$sub_len*2-4);
				$sub .= "...";
			}
			if ($in{'no'} == $no) { $resub = $sub; }
			if ($url) { $url = "&lt;<a href=\"http://$url\">HOME</a>&gt;"; }
			if ($reno) { print '　　'; }
			print "<font color=$sub_color><b>$sub</b></font> Name：<b>$name</b> Date：$date $url <font color=$sub_color>No\.$no</font><br>\n";
			print "<blockquote>$com</blockquote><hr>\n";
		}
	}
	close(IN);

	# タイトル名
	if ($resub !~ /^Re\:/) { $resub = "Re\: $resub"; }

	print <<"EOM";
<a name="RES"></a>
<form action="$script" method="POST">
<input type=hidden name=mode value="regist">
<input type=hidden name=reno value="$in{'no'}">
<blockquote>
EOM
&kakikomi;
	print "</form>\n";
	print "</blockquote>\n</body>\n</html>\n";
	exit;
}
#----------------#
#  デコード処理  #
#----------------#
sub decode {
	local($buffer, @pairs, $name, $value);
	$post_flag=0;
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("投稿量が大きすぎます"); }
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }
	@pairs = split(/&/, $buffer);
	foreach (@pairs) {
		($name,$value) = split(/=/);

		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# 文字コードをシフトJIS変換
		&jcode'convert(*value, "sjis", "", "z");

		# タグ処理
		if ($tagkey) { $value =~ s/<>/&lt;&gt;/g; }
		else {
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ s/\"/&quot;/g;
		}

		# 改行等処理
		if ($name eq "comment") {
			$value =~ s/\r\n/<br>/g;
			$value =~ s/\r/<br>/g;
			$value =~ s/\n/<br>/g;
		} else {
			$value =~ s/\r//g;
			$value =~ s/\n//g;
		}

		# 一括削除用
		if ($name eq "del") { push(@DEL,$value); }

		$in{$name} = $value;
	}
	$mode = $in{'mode'};
	$page = $in{'page'};
	$agent = $ENV{'HTTP_USER_AGENT'};
	$in{'url'} =~ s/^http\:\/\///;
	if ($in{'sub'} eq "") { $in{'sub'} = "無題"; }
}

#----------------------------#
#  掲示板の使い方メッセージ  #
#----------------------------#
sub howto {
	if ($tagkey == 0) {
		$tag_msg = "投稿内容には、<b>タグは一切使用できません。</b>\n";
		} 
		else {
		$tag_msg = "Message欄には、<b>タグ使用をすることができます。</b>\n";
		}
        if ($use_passwd==1) { $passwd_msg = "<LI>この掲示板は<b>会員制</b>です。投稿の際には、<b>「MemberPass」会員パスワードが必要</b>です。投稿をご希望される方は、管理人にメールでお問い合わせください。<p>\n"; 
	}
	&header;
	print <<"EOM";
[<a href="$script?">Back</a>]
<table width="100%">
<tr><th bgcolor=$tbl_color3>
  <font color="#FFFFFF">How To</font>
</th></tr>
</table>
<P><center>
<table width="90%" border=0 cellpadding=10 bgcolor="$tbl_color">
<tr><td bgcolor="$tbl_color2">
<OL>$passwd_msg
<LI>この掲示板は<b>クッキー対応</b>です。１度記事を投稿いただくと、Name、Mail、URL、DeletePassの情報は２回目以降は自動入力されます。（ただし利用者のブラウザがクッキー対応の場合）<P>
<LI>$tag_msg<P>
<LI>記事を投稿する上での必須入力項目は<b>「Name」</b>と<b>「Message」</b>です。Mail、URL、Title、DeletePassは任意です。<P>
<LI>記事には、<b>半角カナは一切使用しないで下さい。</b>文字化けの原因となります。<P>
<LI>記事の投稿時に<b>「DeletePass」</b>にパスワード（英数字で8文字以内）を入れておくと、その記事は次回<b>「DeletePass」</b>によって削除することができます。<P>
<LI>記事の保持件数は<b>最大 $max件</b>です。それを超えると古い順に自動削除されます。<P>
<LI>既存の記事に<b>「返信」</b>をすることができます。各記事の上部にある<b>「Res」</b>ボタンを押すと返信用フォームが現れます。<P>
<LI>過去の投稿記事から<b>「キーワード」によって簡易検索ができます。</b>トップメニューの<a href="$script?mode=find">「Search」</a>のリンクをクリックすると検索モードとなります。<P>
<LI>管理者が著しく不利益と判断する記事や他人を誹謗中傷する記事は予\告なく削除することがあります。
</OL>
</td></tr></table>
</center>
</body>
</html>
EOM
	exit;
}

#------------------#
#  ワード検索処理  #
#------------------#
sub find {
	local($no,$reno,$date,$name,$email,$sub,$com,$url);

	&header;
	print <<"EOM";
[<a href="$script?">Back</a>]
<table width="100%">
<tr><th bgcolor=$tbl_color3>
  <font color="#FFFFFF">Search</font>
</th></tr></table>
<P>
<UL>
  <LI>検索したい<b>キーワード</b>を入力し、「条件」「表\示」を選択して「Search」ボタンを押して下さい。
  <LI>キーワードは「半角スペース」で区切って複数指定することができます。
<P><form action="$script" method="POST">
<input type=hidden name=mode value="find">
キーワード：<input type=text name=word size=30 value="$in{'word'}">
条件：<select name=cond>
EOM
	if (!$in{'cond'}) { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq "$_") {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select>\n 表\示：<select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = $p_log; }
	foreach (5,10,15,20) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select>\n <input type=submit value='Search'></form></UL>\n";

	# ワード検索の実行と結果表示
	if ($in{'word'} ne ""){

		# 入力内容を整理
		$in{'word'} =~ s/　/ /g;
		@pairs = split(/\s+/, $in{'word'});

		# ファイルを読み込み
		@new=();
		open(IN,"$logfile") || &error("Open Error : $logfile");
		$top = <IN>;
		while (<IN>) {
			$flag=0;
			foreach $pair (@pairs) {
				if (index($_,$pair) >= 0) {
					$flag=1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') { $flag=0; last; }
				}
			}
			if ($flag) { push(@new,$_); }
		}
		close(IN);

		# 検索終了
		$count = @new;
		print "検索結果：<b>$count</b>件\n";
		if ($page eq '') { $page = 0; }
		$end_data = @new - 1;
		$page_end = $page + $in{'view'} - 1;
		if ($page_end >= $end_data) { $page_end = $end_data; }

		$next_line = $page_end + 1;
		$back_line = $page - $in{'view'};

		$eword = &url_enc($in{'word'});
		if ($back_line >= 0) {
			print "[<a href=\"$script?mode=find&page=$back_line&word=$eword&view=$in{'view'}&cond=$in{'cond'}\">前の$in{'view'}件</a>]\n";
		}
		if ($page_end ne "$end_data") {
			print "[<a href=\"$script?mode=find&page=$next_line&word=$eword&view=$in{'view'}&cond=$in{'cond'}\">次の$in{'view'}件</a>]\n";
		}
		print "[<a href=\"$script?mode=find\">リセット</a>]\n";

		foreach ($page .. $page_end) {
			($no,$reno,$date,$name,$email,$sub,$com,$url)
							= split(/<>/, $new[$_]);
			if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
			if ($url) { $url = "&lt;<a href=\"http://$url\" target='_blank'>HOME</a>&gt;"; }

			if ($reno) { $no = "$renoへのレス"; }

			# 結果を表示
			print "<hr>[<b>$no</b>] <font color=\"$sub_color\"><b>$sub</b></font>";
			print " Name：<b>$name</b> <small>Date：$date</small> $url<br>\n";
			print "<blockquote>$com</blockquote>\n";
		}
		print "<hr>\n";
	}
	print "</body>\n</html>\n";
	exit;
}

#---------------------------------#
#  ブラウザを判断:フォーム幅調整  #
#---------------------------------#
sub get_agent {
	# ブラウザ名を取得
	$agent = $ENV{'HTTP_USER_AGENT'};

	if ($agent =~ /MSIE 3/i) { 
		$nam_wid = 30;
		$sub_wid = 40;
		$com_wid = 65;
		$url_wid = 48;
		$nam_wid2 = 20;
	} elsif ($agent =~ /MSIE 4/i || $agent =~ /MSIE 5/i) { 
		$nam_wid = 30;
		$sub_wid = 40;
		$com_wid = 60;
		$url_wid = 70;
		$nam_wid2 = 20;
	} else {
		$nam_wid = 20;
		$sub_wid = 25;
		$com_wid = 56;
		$url_wid = 50;
		$nam_wid2 = 10;
	}
}

#------------------#
#  クッキーの発行  #
#------------------#
sub set_cookie {
	# クッキーは60日間有効
	local($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+60*24*60*60);

	@month=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);
	$cook="name<>$in{'name'}\,email<>$in{'email'}\,url<>$in{'url'}\,pwd<>$in{'pwd'}\,icon<>$in{'icon'}\,color<>$in{'color'}\,entry_passwd<>$in{'entry_passwd'}";
	print "Set-Cookie: YYBBS=$cook; expires=$gmt\n";
}

#------------------#
#  クッキーを取得  #
#------------------#
sub get_cookie {
	local($key, $val, @pairs);
	@pairs = split(/;/, $ENV{'HTTP_COOKIE'});
	foreach (@pairs) {
		($key,$val) = split(/=/);
		$key =~ s/\s//g;
		$GET{$key} = $val;
	}
	@pairs = split(/,/, $GET{'YYBBS'});
	foreach (@pairs) {
		($key,$val) = split(/<>/);
		$COOK{$key} = $val;
	}
	$c_name  = $COOK{'name'};
	$c_email = $COOK{'email'};
	$c_url   = $COOK{'url'};
	$c_pwd   = $COOK{'pwd'};
	$c_icon  = $COOK{'icon'};
	$c_color = $COOK{'color'};
        $c_entry_passwd	= $COOK{'entry_passwd'};

	if ($in{'name'})  { $c_name  = $in{'name'}; }
	if ($in{'email'}) { $c_email = $in{'email'}; }
	if ($in{'url'})   { $c_url   = $in{'url'}; }
	if ($in{'pwd'})   { $c_pwd   = $in{'pwd'}; }
	if ($in{'icon'})  { $c_icon  = $in{'icon'}; }
	if ($in{'color'}) { $c_color = $in{'color'}; }
        if ($in{'entry_passwd'})  { $c_entry_passwd  = $in{'entry_passwd'}; }
}
#--------------#
#  エラー処理  #
#--------------#
sub error {
	if ($lockflag) { &unlock; }

	&header if (!$head_flag);
	print "<center><hr width=400><h3>ERROR !</h3>\n";
	print "<P><font color=red>$_[0]</font>\n";
	print "<P><hr width=400></center>\n</body>\n</html>\n";
	exit;
}

#--------------#
#  管理モード  #
#--------------#
sub admin {
	local($dmy,$no,$reno,$date,$name,$mail,$sub,
		$com,$url,$host,$pw,$next_page,$back_page);

	if ($in{'pass'} ne "" && $in{'pass'} ne $pass) {
		&error("DeletePassが違います");
	}

	&header;
	print "[<a href=\"$script?\">Back</a>]\n";
	print "<table width='100%'><tr><th bgcolor=$tbl_color3>\n";
	print "<font color=\"#FFFFFF\">Master</font>\n";
	print "</th></tr></table>\n";

	if ($in{'pass'} eq "") {
		print "<P><center><h4>DeletePassを入力して下さい</h4>\n";
		print "<form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=action value=\"del\">\n";
		print "<input type=password name=pass size=8>";
		print "<input type=submit value=\" Go \"></form>\n";
	}
	else {
		# 削除処理
		if ($DEL[0]) {

			# ロック処理
			if ($lockkey) { &lock; }

			# 削除情報をマッチングし更新
			@new=();
			open(IN,"$logfile") || &error("Open Error : $logfile");
			$top = <IN>;
			while (<IN>) {
				$flag=0;
				($no,$reno,$date) = split(/<>/);
				foreach $del (@DEL) {
					if ($no == $del || $reno == $del) {
						$flag=1; last;
					}
				}
				if ($flag == 0) { push(@new,$_); }
			}
			close(IN);

			# 更新
			unshift(@new,$top);
			open(OUT,">$logfile") || &error("Write Error : $logfile");
			print OUT @new;
			close(OUT);

			# ロック解除
			if ($lockkey) { &unlock; }
		}

		# 管理を表示
		if ($page eq "") { $page = 0; }
		print "<P><center><table><tr><td>\n";
		print "<UL><LI>削除する記事のチェックボックスにチェックを入れ、Deleteボタンを押して下さい。\n";
		print "<LI>親記事を削除するとレス記事も一括して削除されます。</UL>\n";
		print "</td></tr></table>\n";
		print "<form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=page value=\"$page\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=action value=\"$in{'action'}\">\n";
		print "<input type=submit value=\"Delete\">";
		print "<input type=reset value=\"Reset\">\n";
		print "<P><table border=0 cellspacing=1>\n";
		print "<tr><th>Delete</th><th>No</th><th>Date</th><th>Title</th>";
		print "<th>Name</th><th>URL</th><th>Message</th><th>Host</th></tr>\n";

		# ページ区切り処理
		$start = $page + 1;
		$end   = $page + $p_log;

		open(IN,"$logfile") || &error("Open Error : $logfile");
		$top = <IN>;
		$i=0;
		while (<IN>) {
			($no,$reno,$date,$name,$mail,$sub,$com,$url,$host,$pw,)
								 = split(/<>/);
			if ($reno eq "") { $i++; }
			if ($i < $start) { next; }
			if ($i > $end) { last; }

			if ($mail) { $name="<a href=\"mailto:$mail\">$name</a>"; }
			($date,$dmy) = split(/\(/, $date);

			if ($url) { $url = "&lt;<a href=\"http://$url\" target='_blank'>Home</a>&gt;"; }
			else { $url = '-'; }

			$com =~ s/<br>//ig;
			$com =~ s/</&lt;/g;
			$com =~ s/>/&gt;/g;
			if (length($com) > 40) {
				$com = substr($com,0,38);
				$com .= "...";
			}

			if ($reno eq "") { print "<tr><th colspan=8><hr></th></tr>\n"; }

			# 削除チェックボックス
			print "<tr><th><input type=checkbox name=del value=\"$no\"></th>";
			print "<td align=center>$no</td>";
			print "<td><small>$date</small></td><th>$sub</th><th>$name</th>";
			print "<td align=center>$url</td><td><small>$com</small></td>";
			print "<td><small>$host</small></td></tr>\n";

		}
		close(IN);

		print "<tr><th colspan=8><hr></th></tr>\n";
		print "</table></form>\n";
	}

	$next_page = $page + $p_log;
	$back_page = $page - $p_log;

	print "<P><table cellspacing=0 cellpadding=0><tr>\n";
	if ($back_page >= 0) {
		print "<td><form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=page value=\"$back_page\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=action value=\"$in{'action'}\">\n";
		print "<input type=submit value=\"Back$p_log\">\n";
		print "</td></form>\n";
	}
	if ($next_page < $i) {
		print "<td><form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=page value=\"$next_page\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=action value=\"$in{'action'}\">\n";
		print "<input type=submit value=\"Next$p_log\">\n";
		print "</td></form>\n";
	}
	print "</tr></table></center>\n</body>\n</html>\n";
	exit;
}

#------------------#
#  ユーザ記事削除  #
#------------------#
sub usr_del {
	local(@lines,@new,$no,$reno,$dt,$name,$mail,$sub,$com,$url,$host,$pw,$top,$PW);

	# POST限定
	if (!$post_flag) { &error("不正なアクセスです"); }

	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("記事NoまたはDeletePassが入力モレです"); }

	# ロック処理
	if ($lockkey) { &lock; }

	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);
	$top = shift(@lines);

	$flag=0;
	foreach (@lines) {
		($no,$reno,$dt,$name,$mail,$sub,$com,$url,$host,$pw) = split(/<>/);

		if ($flag == 0 && $in{'no'} == $no) {
			$PW = $pw;
			if ($reno eq "") { $flag=2; }
			else { $flag=1; }
		}
		elsif ($flag == 2 && $in{'no'} == $reno) { next; }
		else { push(@new,$_); }
	}

	if ($flag == 0) { &error("該当記事が見当たりません"); }
	if ($PW eq '') { &error("該当記事にはDeletePassが設定されていません"); }

	# パスワードを照合
	$match = &decrypt("$in{'pwd'}","$PW");
	if ($match ne 'yes') { &error("DeletePassが違います"); }

	# 更新
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	if ($lockkey) { &unlock; }
}

#----------------#
#  記事修正処理  #
#----------------#
sub usr_edt {
	local($no,$reno,$dt,$name,$mail,$sub,$com,
		$url,$host,$pw,$color,$icon,$flag,$top,$flag,$pattern);

	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("記事NoまたはDeletePassが入力モレです"); }

	if ($in{'action'} eq "edit") {
		# フォーム入力チェック
		&form_check;

		# ロック処理
		&lock if ($lockkey);
	}

	$flag=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$reno,$dt,$name,$mail,$sub,$com,$url,$host,$pw,$color,$icon)
									 = split(/<>/);
		if ($in{'no'} == $no) {
			$pw2 = $pw;
			$flag=1;
			if ($in{'action'} ne "edit") { last; }
			else {
				if ($autolink) { &auto_link($in{'comment'}); }
				$_ = "$no<>$reno<>$dt<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pw<>$in{'color'}<>$in{'icon'}<>$agent<>\n";
			}
		}
		if ($in{'action'} eq "edit") { push(@new,$_); }
	}
	close(IN);
	if (!$flag) { &error("該当の記事が見当たりません"); }
	if ($pw2 eq "") { &error("DeletePassが設定されていません"); }
	$check = &decrypt("$in{'pwd'}", "$pw2");
	if ($check ne "yes") { &error("DeletePassが違います"); }
	if ($in{'action'} eq "edit") {
		unshift(@new,$top);
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);

		&unlock if ($lockkey);
		&set_cookie;

		if ($in{'url'}) { $in{'url'} = "<a href=\"http://$in{'url'}\" target=\"_blank\">http://$in{'url'}</a>"; }
		if ($in{'email'}) { $in{'email'} = "<a href=\"mailto:$in{'email'}\">$in{'email'}</a>"; }

		&header;
		print "<div align=center>\n";
		print "<b>- 以下のとおり修正が完了しました -</b>\n";
		print "<P><table border=0 cellpadding=10 width='85%' bgcolor=\"$tbl_color\"><tr><td bgcolor=\"$tbl_color2\">\n";
		print "Name：<b>$in{'name'}</b><br>\n";
		print "Mail：$in{'email'}<br>\n";
		print "Title：<b>$in{'sub'}</b><br>\n";
		print "URL：$in{'url'}</tt><P>\n";
		print "Massage：<font color=\"$in{'color'}\">$in{'comment'}</font>\n";
		print "</td></tr></table>\n";
		print "<P><form action=\"$script\">\n";
		print "<input type=submit value=' List '></form>\n";
		print "</div>\n</body>\n</html>\n";
		exit;
	}

	&get_agent;
	$com =~ s/<br>/\r/g;
	$pattern = 'http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+';
	$com =~ s/<a href="$pattern" target='_blank'>($pattern)<\/a>/$1/go;
	$com =~ s/&lt;/</g;
	$com =~ s/&gt;/>/g;
	$com =~ s/&quot;/\"/g;
	$c_name = $name;
	$c_email= $mail;
	$resub = $sub;
	$FORM{'MSGBODY'} = $com;
	$c_url = $url;

	if ($ImageView == 1) { &header('ImageUp'); }
	else { &header; }
	print <<"EOM";
<b>- 変更する部分のみ修正してSubmitボタンを押して下さい -</b>
<P>
<form action="$script" method="POST">
<input type=hidden name=mode value="usr_edt">
<input type=hidden name=action value="edit">
<input type=hidden name=pwd value="$in{'pwd'}">
<input type=hidden name=no value="$in{'no'}">
EOM
	&kakikomi;
	print "  </form></center>\n</body>\n</html>\n";
	exit;
}

#------------------------#
#  フォーム入力チェック  #
#------------------------#
sub form_check {
	local($ref_url);

	# POST限定
	if (!$post_flag) { &error("不正なアクセスです"); }

	# 参照元のチェック
	if ($ref_chk2) {
		$ref_url = $ENV{'HTTP_REFERER'};
		$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($ref_url !~ /$cgi_url/i) { &error("参照元が不正です"); }
	}

	# 名前とMessageは必須
	if ($in{'name'} eq "") { &error("名前が入力されていません"); }
	if ($in{'comment'} eq "") { &error("Messageが入力されていません"); }
	if ($in_email && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,3}/) {
		&error("Mailの入力内容が正しくありません");
	}

	# 管理アイコンのチェック
	if ($my_icon && $in{'icon'} eq $my_gif) {
		if ($in{'pwd'} ne $pass) { &error("管理用アイコンは管理者専用です"); }
	}
}

#--------------#
#  時間を取得  #
#--------------#
sub get_time {
	$ENV{'TZ'} = "JST-9";   ####"Japan";
	$times = time;
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($times);
	@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 日時のフォーマット
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$week[$wday],$hour,$min);
}
#--------------------#
#  プロクシチェック  #
#--------------------#
sub proxy {
  if ($plevel == 1) { # 制限レベル「弱」の場合
    if ($xfor !~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/) { # IP漏れしている場合は許可
      if ($host =~ /squid|^firewall|proxy|cache|delegate|^dns|keeper|^mail|^www|^ns\d{0,2}\.|us$|uk$|edu$|com$|org$|net$|at$|au$|ca$|ch$|de$|dk$|fi$|fr$|it$|il$|kr$|nl$|pt$|tw$/i && $host !~/^yahoo/i ) {
        &error("プロクシ制限中");
      }
      if ($via  ne "") { &error("プロクシ制限中"); }
      if ($xfor ne "") { &error("プロクシ制限中"); }
      if ($for  ne "") { &error("プロクシ制限中"); }
      if ($agent =~ /via|squid|delegate|httpd|proxy|cache/i){ &error("プロクシ制限中"); }
    }
  } 
  else  { # 制限レベル「強」の場合
    if($host ne $addr && $host !~ /jp$/i && $host !~/^yahoo/i) { # jpドメインじゃない場合（ＩＰ串も）アウト！
      &error("プロクシ制限中");} 
    if ($host =~ /squid|^firewall|proxy|cache|delegate|^dns|keeper|^mail|^www|^ns\d{0,2}\./i) {
      &error("プロクシ制限中"); }
    if ($via  ne "") { &error("プロクシ制限中"); }
    if ($xfor ne "") { &error("プロクシ制限中"); }
    if ($for  ne "") { &error("プロクシ制限中"); }
    if ($agent=~ /via|squid|delegate|httpd|proxy|cache/i) { &error("プロクシ制限中");}
    if ($ENV{'HTTP_PROXY_CONNECTION'} ne "") { &error("プロクシ制限中"); }
    if ($ENV{'HTTP_CACHE_INFO'}       ne "") { &error("プロクシ制限中"); }
  }
}

#----------------------------#
#    漏れＩＰアドレス取得    #
#----------------------------#
sub getip {
  $sp_host   = $ENV{'HTTP_SP_HOST'};
  $client_ip = $ENV{'HTTP_CLIENT_IP'};
  $http_from = $ENV{'HTTP_FROM'};

  $trueip = $sp_host   if ($sp_host ne "");
  $trueip = $via       if ($via =~ s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/);
  if( $client_ip=~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/ ){
    $trueip = $client_ip;
  }elsif( $client_ip=~ s/^([\dA-F]{2})([\dA-F]{2})([\dA-F]{2})([\dA-F]{2})/$1$2$3$4/i){
    $client_ip = join('.', hex($1), hex($2), hex($3), hex($4)); 
    $trueip = $client_ip;
  }
  $trueip = $for       if ($for =~ s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/);
  $trueip = $xfor      if ($xfor =~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/);
  $trueip = $http_from if ($http_from ne "");
  return $trueip;
}

#--------------------#
#  アクセスログ取得  #
#--------------------#
sub acount {
  $cook = $ENV{'HTTP_COOKIE'};
  $ref_url = $ENV{'HTTP_REFERER'};
  if ( !open(LOG, "$access_log") ) { &error("アクセスログ・エラー"); }
  @lines = <LOG>;
  close(LOG);
  $kiroku_data = "[$date] $ref_url - $host - $addr - $via - $trueip - $agent - $cook \n";
  unshift(@lines, "$kiroku_data");
  pop @lines while @lines > $rescue;
  if ( !open(LOG,">$access_log") ) { &error("アクセスログ・エラー"); }
  print LOG @lines;
  close(LOG);
}

#----------------#
#  カウンタ処理  #
#----------------#
sub counter {
	local($cntup,@cnts,$cnt);

	# 閲覧時のみカウントアップ
	#if ($mode eq '') { $cntup=1; } else { $cntup=0; }
	$cntup=1;

	# カウントファイルを読みこみ
	open(IN,"$cntfile") || &error("Open Error : $cntfile");
	eval "flock(IN, 1);";
	$data = <IN>;
	close(IN);

	# IPチェックとログ破損チェック
	($cnt, $ip) = split(/:/, $data);
	#if ($addr eq $ip || $cnt eq "") { $cntup=0; }
	if ($cnt eq "") { $cntup=0; }
	
	# カウントアップ
	if ($cntup) {
		$cnt++;
		open(OUT,"+< $cntfile") || &error("Write Error : $cntfile");
		eval "flock(OUT, 2);";
		truncate(OUT, 0);
		seek(OUT, 0, 0);
		print OUT "$cnt\:$addr";
		close(OUT);
	}

	# 桁数調整
	while(length($cnt) < $mini_fig) { $cnt = '0' . $cnt; }
	@cnts = split(//, $cnt);

	# GIFカウンタ表示
	if ($counter == 2) {
		foreach (0 .. $#cnts) {
			print "<img src=\"$gif_path$cnts[$_]\.gif\" alt=\"$cnts[$_]\" width=\"$mini_w\" height=\"$mini_h\">";
		}
	}
	# テキストカウンタ表示
	else {
		print "<font color=\"$cnt_color\" face=\"verdana,Times New Roman,Arial\">$cnt</font><br>\n";
	}
}

#--------------#
#  ロック処理  #
#--------------#
sub lock {
	local($retry,$mtime);

	# 1分以上古いロックは削除する
	if (-e $lockfile) {
		($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	# symlink関数式ロック
	if ($lockkey == 1) {
		$retry = 5;
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		$retry = 5;
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
	$lockflag=0;
}

#--------------#
#  メール送信  #
#--------------#
sub mail_to {
	local($MailSub,$MailBody,$email);

	# メールタイトルを定義
	$MailSub = "[$title : $no] $in{'sub'}";

	# URL情報
	if ($in{'url'}) { $hp = "http://$in{'url'}"; }
	else { $hp = ""; }

	# 記事の改行・タグを復元
	$com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	$com =~ s/&lt;/</g;
	$com =~ s/&gt;/>/g;
	$com =~ s/&quot;/\"/g;

	# メール本文を定義
	$MailBody = <<"EOM";
Date：$date
Host：$host
Agent：$ENV{'HTTP_USER_AGENT'}
Name：$in{'name'}
Mail：$in{'email'}
URL  ：$hp
Title：$in{'sub'}
Message：
$com
EOM
	# JISコード変換
    	&jcode'convert(*MailSub,'jis');
    	&jcode'convert(*MailBody,'jis');

	# メールアドレスがない場合はダミーメールに置き換え
	if ($in{'email'} eq "") { $email = 'nomail@xxx.xxx'; }
	else { $email = $in{'email'}; }
	open(MAIL,"| $sendmail -t") || &error("メール送信に失敗しました");
	print MAIL "To: $mailto\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $MailSub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL "$MailBody\n";
	close(MAIL);
}

#----------------------#
#  パスワード暗号処理  #
#----------------------#
sub encrypt {
	local($inpw) = $_[0];
	local(@SALT, $salt, $encrypt);

	@SALT = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $SALT[int(rand(@SALT))] . $SALT[int(rand(@SALT))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}

#----------------------#
#  パスワード照合処理  #
#----------------------#
sub decrypt {
	local($inpw, $logpw) = @_;
	local($salt, $key, $check);

	$salt = $logpw =~ /^\$1\$(.*)\$/ && $1 || substr($logpw, 0, 2);
	$check = "no";
	if (crypt($inpw, $salt) eq $logpw || crypt($inpw, '$1$' . $salt) eq $logpw)
		{ $check = "yes"; }
	return $check;
}

#------------------#
#  HTMLのヘッダー  #
#------------------#
sub header {
	$head_flag=1;
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<STYLE type="text/css">
<!--
body,tr,td,th { font-size: $b_size }
a:hover { color: $alink }
span { font-size: $t_size }
big  { font-size: 12pt }
small { font-size: 9pt }
-->
</STYLE>
EOM
	# JavaScriptヘッダー
	if ($ImageView == 1 && $_[0] eq "ImageUp") {
		print "<META http-equiv=\"Content-Script-Type\" content=\"text/javascript\">\n";
		print "<SCRIPT type=\"text/javascript\">\n";
		print "<!--\n";
		print "function ImageUp() {\n";
		print "window.open(\"$script?mode=image\",\"window1\",\"width=$img_w,height=$img_h,scrollbars=1\");\n}\n//-->\n</SCRIPT>\n";
	}

	print "<title>$title</title></head>\n";
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
}

#-----------------#
#  自動URLリンク  #
#-----------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target='_blank'>$2<\/a>/g;
}

#--------------------#
#  画像イメージ表示  #
#--------------------#
sub image {
	local($i,$j,$stop);

	&header;
	print "<center><hr width=\"75%\">\n";
	print "<b><big>画像イメージサンプル</big></b>\n";
	print "<P><small>- 現在登録されている画像イメージは以下のとおりです -</small>\n";
	print "<hr width=\"75%\">\n";
	print "<P><table border=1 cellpadding=5 cellspacing=0><tr>\n";

	$i=0; $j=0;
	$stop = @icon1;
	foreach (0 .. $#icon1) {
		$i++; $j++;
		print "<th><img src=\"$imgurl$icon1[$_]\" ALIGN=middle alt=\"$icon1[$_]\"> $icon2[$_]</th>\n";
		if ($j != $stop && $i >= 5) { print "</tr><tr>\n"; $i=0; }
		elsif ($j == $stop) {
			if ($i == 0) { last; }
			while ($i < 5) { print "<th><br></th>"; $i++; }
		}
	}

	print "</tr></table><br>\n";
	print "<FORM><INPUT TYPE=\"button\" VALUE=\"  CLOSE  \" onClick=\"top.close();\"></FORM>\n";
	print "</center>\n</body>\n</html>\n";
	exit;
}

#----------------#
#  ホスト名取得  #
#----------------#
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if (($host eq $addr) || ($host eq '')) { 
  		$host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr;
	}
}

#----------------#
#  過去ログ生成  #
#----------------#
sub pastlog {
	local($count,$pastfile,@temp,$pno,$preno,$pdate,$pname,$pmail,$psub,$pcom,$purl,$pho);
	local($past_flag)=0;

	# 過去NOを開く
	open(NO,"$nofile") || &error("Open Error : $nofile");
	$count = <NO>;
	close(NO);

	# 過去ログのファイル名を定義
	$pastfile = "$pastdir$count\.dat";

	# 過去ログを開く
	open(IN,"$pastfile") || &error("Open Error : $pastfile");
	@past = <IN>;
	close(IN);

	# 規定の行数をオーバーすると次ファイルを自動生成
	if ($#past > $log_line) {
		$past_flag=1;

		# カウントファイル更新
		$count++;
		open(NO,">$nofile") || &error("Write Error : $nofile");
		print NO $count;
		close(NO);

		$pastfile = "$pastdir$count\.dat";
		@past=();
	}

	@temp=();
	foreach (@data) {
		($pno,$preno,$pdate,$pname,$pmail,$psub,$pcom,$purl,$pho)
								 = split(/<>/);
		if ($pmail) { $pname = "<a href=\"mailto:$pmail\">$pname</a>"; }
		if ($purl) { $purl = "&lt;<a href=\"http://$purl\" target='_blank'>HOME</a>&gt;"; }
		if ($preno) { $pno = "$prenoへのレス"; }

		# 保存記事をフォーマット
		push(@temp,"<hr>[$pno] <font color=\"$sub_color\"><b>$psub</b></font> Name：<b>$pname</b> <small>Date：$pdate</small> $purl<br><blockquote>$pcom</blockquote><!-- $pho -->\n");
	}

	# 過去ログを更新
	unshift(@past,@temp);
	open(OUT,">$pastfile") || &error("Write Error : $pastfile");
	print OUT @past;
	close(OUT);

	if ($past_flag) { chmod(0666,$pastfile); }
}

#------------#
#  過去ログ  #
#------------#
sub past {
	local($pastno,@new,$count,@pairs,$pair);

	open(IN,"$nofile") || &error("Open Error : $nofile");
	$pastno = <IN>;
	close(IN);

	if (!$in{'pastlog'}) { $in{'pastlog'} = $pastno; }

	&header;
	print <<"EOM";
[<a href="$script?">Back</a>]
<table width="100%"><tr><th bgcolor=$tbl_color3>
  <font color="#FFFFFF">Log[$in{'pastlog'}]</font>
</th></tr></table>
<P><table><tr><td>
<form action="$script" method="POST">
<input type=hidden name=mode value=past>
過去ログ：<select name=pastlog>
EOM

	$pastkey = $pastno;
	while ($pastkey > 0) {
		if ($in{'pastlog'} == $pastkey) {
			print "<option value=\"$pastkey\" selected>$pastkey Page\n";
		} else {
			print "<option value=\"$pastkey\">$pastkey Page\n";
		}
		$pastkey--;
	}
	print "</select>\n<input type=submit value='Go'></td></form>\n";
	print "<td width=30></td><td>\n";
	print "<form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=past>\n";
	print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
	print "キーワード：<input type=text name=word size=30 value=\"$in{'word'}\">\n";
	print "条件：<select name=cond>\n";

	foreach ('AND', 'OR') {
		if ($in{'cond'} eq "$_") {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select>\n";
	print "表\示：<select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = $p_log; }
	foreach (5,10,15,20,25,30) {
		if ($in{'view'} eq "$_") {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select>\n<input type=submit value='Search'></td></form>\n";
	print "</td></tr></table>\n";

	# 表示ログを定義
	$in{'pastlog'} =~ s/\D//g;
	$file = "$pastdir$in{'pastlog'}\.dat";

	# ワード検索処理
	if ($in{'word'} ne "") {
		$in{'word'} =~ s/　/ /g;
		@pairs = split(/\s+/, $in{'word'});

		@new=();
		open(IN,"$file") || &error("Open Error : $file");
		while (<IN>) {
			$flag=0;
			foreach $pair (@pairs) {
				if (index($_,$pair) >= 0) {
					$flag=1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') { $flag=0; last; }
				}
			}
			if ($flag) { push(@new,$_); }
		}
		close(IN);

		$count = @new;
		print "検索結果：<b>$count</b>件\n";
		if ($page eq '') { $page = 0; }
		$end_data = @new - 1;
		$page_end = $page + $in{'view'} - 1;
		if ($page_end >= $end_data) { $page_end = $end_data; }

		$next_line = $page_end + 1;
		$back_line = $page - $in{'view'};

		$eword = &url_enc($in{'word'});
		if ($back_line >= 0) {
			print "[<a href=\"$script?mode=past&page=$back_line&word=$eword&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">前の$in{'view'}件</a>]\n";
		}
		if ($page_end ne "$end_data") {
			print "[<a href=\"$script?mode=past&page=$next_line&word=$eword&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">次の$in{'view'}件</a>]\n";
		}
		print "[<a href=\"$script?mode=past&pastlog=$in{'pastlog'}\">検索やり直し</a>]\n";

		# 表示開始
		foreach ($page .. $page_end) {
			print $new[$_];
		}
		print "<hr>\n</body>\n</html>\n";
		exit;
	}

	# ページ区切り処理
	$start = $page + 1;
	$end   = $page + $p_log;

	$i=0;
	open(IN,"$file") || &error("Open Error : $file");
	while (<IN>) {
		$flag=0;
		if ($_ =~ /^\<hr\>\[\d+\]/) { $flag=1; $i++; }
		if ($i < $start) { next; }
		if ($i > $end) { last; }

		if ($flag) { print $_; }
		else {
			$_ =~ s/<hr>//ig;
			print "<blockquote>$_</blockquote>\n";
		}
	}
	close(IN);
	print "<hr>\n";

	$next_page = $page + $p_log;
	$back_page = $page - $p_log;

	print "<table>\n";
	if ($back_page >= 0) {
		print "<td><form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$back_page\">\n";
		print "<input type=submit value=\"前の$p_log件\">\n";
		print "</td></form>\n";
	}
	if ($next_page < $i) {
		print "<td><form action=\"$script\" method=POST>\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$next_page\">\n";
		print "<input type=submit value=\"次の$p_log件\">\n";
		print "</td></form>\n";
	}
	print "</table>\n</body>\n</html>\n";
	exit;
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	&header;
	print "<h2>Check Mode</h2>\n";
	print "<UL>\n";

	# ログパス
	if (-e $logfile) { print "<LI>ログファイルのパス：OK\n"; }
	else { print "<LI>ログファイルのパス：NG → $logfile\n"; }

	# ログパーミッション
	if (-r $logfile && -w $logfile) { print "<LI>ログファイルのパーミッション：OK\n"; }
	else { print "<LI>ログファイルのパーミッション：NG\n"; }

	# カウンタログ
	print "<LI>カウンタ：";
	if ($counter) {
		print "設定あり\n";
		if (-e $cntfile) { print "<LI>カウンタログファイルのパス：OK\n"; }
		else { print "<LI>カウンタログファイルのパス：NG → $cntfile\n"; }
	}
	else { print "設定なし\n"; }

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 0) { print "ロック設定なし\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }

		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) { print "<LI>ロックディレクトリのパス：OK\n"; }
		else { print "<LI>ロックディレクトリのパス：NG → $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>ロックディレクトリのパーミッション：OK\n";
		} else {
			print "<LI>ロックディレクトリのパーミッション：NG → $lockdir\n";
		}
	}

	# 過去ログ
	print "<LI>Log：";
	if ($pastkey == 0) { print "設定なし\n"; }
	else {
		print "設定あり\n";

		# NOファイル
		if (-e $nofile) { print "<LI>NOファイルパス：OK\n"; }
		else { print "<LI>NOファイルのパス：NG → $nofile\n"; }
		if (-r $nofile && -w $nofile) { print "<LI>NOファイルパーミッション：OK\n"; }
		else { print "<LI>NOファイルパーミッション：NG → $nofile\n"; }

		# ディレクトリ
		if (-d $pastdir) { print "<LI>過去ログディレクトリパス：OK\n"; }
		else { print "<LI>過去ログディレクトリのパス：NG → $pastdir\n"; }
		if (-r $pastdir && -w $pastdir && -x $pastdir) {
			print "<LI>過去ログディレクトリパーミッション：OK\n";
		} else {
			print "<LI>過去ログディレクトリパーミッション：NG → $pastdir\n";
		}
	}

	print "</UL>\n</body>\n</html>\n";
	exit;
}

#-----------------#
#  URLエンコード  #
#-----------------#
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}
