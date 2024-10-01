use strict;
use warnings;
use IO::Socket::INET;
use open ':std', ':encoding(UTF-8)';

sub chatscript {
    my ($mensaje, $usuario, %opts) = @_;
    my $botname = $opts{botname} // '';
    my $ip = $opts{ip} // '127.0.0.1';
    my $port = $opts{port} // 1024;
    my $buffer_size = $opts{buffer_size} // 2048;
    my $mje_send = "$usuario\0$botname\0$mensaje\0";
    utf8::encode($mje_send);
    my $client = IO::Socket::INET->new(
        PeerHost => $ip,
        PeerPort => $port,
        Proto    => 'tcp',
    ) or die "Error al conectarse al servidor: $!\n";
    print $client "$mje_send
";
    shutdown($client, 1);
    my $respuesta = '';
    while (my $linea = <$client>) {
        $respuesta .= $linea;
    }
    close($client);
    $respuesta =~ s/^\n//;
    $respuesta =~ s/\n$//;
    utf8::decode($respuesta);
    return $respuesta;
}

use Getopt::Long qw(GetOptions);

my %opts;
GetOptions(
    'botname=s' => \$opts{botname},
    'ip=s' => \$opts{ip},
    'port=i' => \$opts{port},
    'buffer_size=i' => \$opts{buffer_size},
);
my ($mensaje, $usuario) = @ARGV;
my $respuesta = chatscript($mensaje, $usuario, %opts);

# Validate response
if ($respuesta =~ /No such bot\./) {
    die "Error: No such bot.";
}

# Print response from bot
print "Response: $respuesta
";

