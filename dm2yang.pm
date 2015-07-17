# BBF report tool plugin to process a DM Instance and map it to one or more
# YANG modules
#
# based on ideas (and some code) from the standard MAP plugin

# example invocation:
# TBD

# XXX output should be piped through the rfcstrip utility, which will process
#     <CODE BEGINS> and <CODE ENDS> lines

# XXX do we want to do any name mapping, e.g. ProfileLevel -> profile-level? i
#     think not

package dm2yang;

use strict;

# XXX uncomment to enable traceback on warnings and errors
#use Carp::Always;

use Data::Dumper;
use Text::Format;

# parse config file
sub dm2yang_init {
}

# YANG modules array
my $modules = [];

# current YANG module
my $module = undef;

# this is called for each node
sub dm2yang_node {
    my ($node, $indent) = @_;

    my $type = $node->{type};
    my $name = $node->{name};
    my $access = $node->{access};
    my $description = $node->{description};
    my $syntax = $node->{syntax};

    # convert as appropriate for YANG
    # XXX need to be able to pick up such things from the config file
    # XXX defaults should be applied later?
    $name =~ s/:\d+\.\d+$//;    

    # XXX default file name should come from module and name and revision?
    my $file = qq{$name.yang};
    my $namespace = qq{urn:tbd};
    my $prefix = qq{TBD};
    my $organization = qq{TBD};
    my $contact = qq{TBD};
    my $revdate = qq{1970-01-01};
    my $revdesc = qq{TBD};
    my $revref = qq{TBD};

    # a new YANG module can be triggered by a model or by an object
    # XXX initially a YANG module is triggered only by a model
    # XXX also need to decide how to handle biblio and types
    if ($type eq 'model') {
        $module = {
            node => $node,
            file => $file,
            name => $name,
            namespace => $namespace,
            prefix => $prefix,
            organization => $organization,
            contact => $contact,
            description => $description,
            revdate => $revdate,
            revdesc => $revdesc,
            revref => $revref,
            nodes => []
        };
        push @$modules, $module;
    }

    # use objects and parameters
    my $use_node = $type eq 'object' || $syntax;

    # ignore #entries and Alias parameters
    # XXX Alias parameters are a real problem because they are always writable
    #     and therefore can force a sub-tree that really should be config false
    #     to be config true
    # XXX we are not going to be able to avoid creating separate config and
    #     status trees
    my $ignore_node = $syntax && ($node->{table} || $node->{name} eq 'Alias');

    if ($use_node && !$ignore_node) {
        push @{$module->{nodes}}, $node;

        # set the dm2yang_config property here and, if true, propagate it up
        # the tree
        $node->{dm2yang_config} = $access && $access eq 'readWrite';
        if ($node->{dm2yang_config}) {
            for (my $pnode = $node->{pnode};
                 $pnode; $pnode = $pnode->{pnode}) {
                $pnode->{dm2yang_config} = 1;
            }
        }
    }
}

# this is called after all nodes have been processed
sub dm2yang_end {
    my ($node, $indent) = @_;

    # process nodes
    process_nodes($node);
    
    # output modules
    output_modules($modules);
}

# this does one-off processing of the node tree
# XXX this might not be necessary
sub process_nodes {
    my ($root) = @_;
}

# forward declarations
sub output_module;
sub output_module_preamble_open;
sub output_imports;
sub output_includes;
sub output_module_preamble_continue;
sub output_extensions;
sub output_features;
sub output_identities;
sub output_typedefs;
sub output_groupings;
sub output_data_definitions;
sub output_augments;
sub output_rpcs;
sub output_notifications;
sub output_module_preamble_close;
sub output;

# output modules
sub output_modules {
    my ($modules) = @_;
    
    my $i = 0;

    foreach my $module (@$modules) {
        output_module $i, $module;
    }
}

# output a module
sub output_module {
    my ($i, $module) = @_;
    
    output_module_preamble_open $i, $module;
    $i++;
    
    output_imports $i, $module;
    output_includes $i, $module;

    # note that this is called with incremented indentation
    output_module_preamble_continue $i, $module;

    output_extensions $i, $module;
    output_features $i, $module;
    output_identities $i, $module;
    output_typedefs $i, $module;
    output_groupings $i, $module;
    output_data_definitions $i, $module;
    output_augments $i, $module;
    output_rpcs $i, $module;
    output_notifications $i, $module;

    $i--;
    output_module_preamble_close $i, $module;    
}

# output module module_preamble (open, continue, close)
sub output_module_preamble_open {
    my ($i, $module) = @_;
    
    my $file = $module->{file};
    my $name = $module->{name};
    my $namespace = $module->{namespace};
    my $prefix = $module->{prefix};

    output $i, qq{
<CODE BEGINS> file "$file"
module $name \{
  namespace "$namespace";
  prefix $prefix;
};
}

sub output_module_preamble_continue {
    my ($i, $module) = @_;
    
    my $organization = $module->{organization};
    my $contact = $module->{contact};
    my $description = $module->{description};
    my $revdate = $module->{revdate};
    my $revdesc = $module->{revdesc};
    my $revref = $module->{revref};

    output $i, qq{

organization
  "$organization";

contact
  "$contact";

description
  "$description";

revision $revdate {
  description
    "$revdesc";
  reference
    "$revref";
}
};
}

sub output_module_preamble_close {
    my ($i, $module) = @_;
    
    output $i, qq{
\}
<CODE ENDS>
};
}

# output module imports
sub output_imports {
    my ($i, $module) = @_;

    my $node = $module->{node};

    # XXX this logic is adapted from main::xml2_node
    #my $lfile = $node->{lfile};
    #my $limports = $main::imports->{$lfile};
    #main::tmsg Dumper($limports);

    # XXX for now we will hard code an import of the ietf-yang-types module
    # XXX for now we will hard code an import of the tr-106-types module; in
    #     general we will never need to import previous minor versions because
    #     YANG doesn't define deltas in the same way as DM; we will need to
    #     work out how to import other auto-generated modules
    # XXX obviously we won't import this module when IT is being generated!
    # XXX auto-imports run the risk of "imported module not used" warnings
    output $i, qq{

import ietf-yang-types {
  prefix yang;
}

import tr-106-types {
  prefix types;
}
};
}

# output module includes
# XXX don't currently use sub-modules, so there are never any includes
sub output_includes {
    my ($i, $module) = @_;
    
}

# output module extensions
# XXX should look at whether can use extensions to indicate use of mediawiki
#     description markup
sub output_extensions {
    my ($i, $module) = @_;
    
}

# output module features
sub output_features {
    my ($i, $module) = @_;
    
}

# output module identities
sub output_identities {
    my ($i, $module) = @_;
    
}

# output module typedefs
sub output_typedefs {
    my ($i, $module) = @_;
    
}

# output module groupings
sub output_groupings {
    my ($i, $module) = @_;
    
}

# output module data definitions
sub output_subtree;
sub output_container_open;
sub output_list_open;
sub output_leaf;
sub output_container_close;
sub output_list_close;
sub output_data_definitions {
    my ($i, $module) = @_;
    
    my $nodes = $module->{nodes};

    # XXX might not need this, but will leave it for now
    my $state = {};

    output_subtree $i, $nodes, 0, $state;
}

sub output_subtree {
    my ($i, $nodes, $j, $state) = @_;

    # return immediately if no more nodes
    my $node = $nodes->[$j];
    return unless $node;

    my $type = $node->{type};
    my $path = $node->{path};

    # parameter -> leaf
    # XXX or leaf-list
    if ($type ne 'object') {
        output_leaf $i, $node, $state;
    }

    # object -> container or list
    else {
        my $table = $path =~ /\.\{i\}\.$/;
        if (!$table) {
            output_container_open $i, $node, $state;
        } else {
            output_list_open $i, $node, $state;
        }

        # continue while next node path is a prefix of the first node's path
        while ($nodes->[$j+1] && index($nodes->[$j+1]->{path}, $path) >= 0) {
            $j = output_subtree $i+1, $nodes, $j+1, $state;
        }

        if (!$table) {
            output_container_close $i, $node, $state;
        } else {
            output_list_close $i, $node, $state;
        }
    }

    # return index of last node processed
    return $j;
}

sub output_container_open {
    my ($i, $node, $state) = @_;

    my $name = $node->{name};

    $name =~ s/\.$//;

    output $i, qq{};
    output $i, qq{container $name \{};

    my $config = get_config($node, $state);
    output $i+1, $config if $config;

    my $status = get_status($node, $state);
    output $i+1, $status if $status;

    my $description = get_description($node, $i+2, $state);
    output $i+1, $description if $description;
}

sub output_list_open {
    my ($i, $node, $state) = @_;

    my $name = $node->{name};
    my $access = $node->{access};
    my $minEntries = $node->{minEntries};
    my $maxEntries = $node->{maxEntries};
    my $uniqueKeys = $node->{uniqueKeys};
    
    $name =~ s/\.\{i\}\.$//;

    output $i, qq{};
    output $i, qq{list $name \{};

    # prefer the first functional unique key as "key" and any others as
    # "unique"
    # XXX this logic is adapted from main:xml2_node
    # XXX if no unique keys for writable table (config true), should invent an
    #     "instanceNumber" one?
    # XXX need to exclude Alias because Alias parameters are ignored
    # XXX should use a helper to decide when need to quote, e.g. here only
    #     needed when the key involves multiple parameters
    # XXX should use a get_key routine; combine with get_unique?
    my $key = qq{};
    if ($uniqueKeys) {
        ($key) = grep {$_->{functional}} @$uniqueKeys;
        ($key) = grep {!$_->{functional}} @$uniqueKeys unless $key;       
        if ($key) {
            my $temp = join ' ', @{$key->{keyparams}};
            $key = qq{key "$temp";};
        }
    }
    output $i+1, $key if $key;

    my $config = get_config($node, $state);
    output $i+1, $config if $config;

    my $status = get_status($node, $state);
    output $i+1, $status if $status;

    my $min_elements = $minEntries > 0 ?
        qq{min-elements $minEntries;} : qq{};
    output $i+1, $min_elements if $min_elements;

    my $max_elements = $maxEntries ne 'unbounded' ?
        qq{max-elements $maxEntries;} : qq{};    
    output $i+1, $max_elements if $max_elements;

    my $description = get_description($node, $i+2, $state);
    output $i+1, $description if $description;
}

sub output_leaf {
    my ($i, $node, $state) = @_;

    my $name = $node->{name};
    my $type = $node->{type};
    my $syntax = $node->{syntax};    

    output $i, qq{leaf $name \{};

    my $status = get_status($node, $state);
    output $i+1, $status if $status;

    # XXX should put this into get_type
    # XXX this logic is adapted from main::type_string
    my $typeinfo = main::get_typeinfo($type, $syntax);
    ($type, my $dataType) = ($typeinfo->{value}, $typeinfo->{dataType});

    # map DM types to YANG types
    # XXX yang:data-and-time might not have exactly the same semantics as
    #     DM dateTime, e.g. wrt the unknown time; here the right thing to do
    #     is probably to sub-class it and define the special values in the
    #     sub-class?
    # XXX yang:hex-string is different from DM hexBinary in that it uses colon
    #     separators and is regarded as a string, so its length is hex digits
    #     not octets
    # XXX UUID is not a primitive DM type, and its representation doesn't
    #     include hyphens, but there is a standard yang:uuid, so it probably
    #     makes sense to use it
    # XXX there are some more hard-coded types, e.g. Alias and IPAddress,
    #     pending doing a proper job with DM imports
    my $dm_to_yang_type_map = {
        base64 => 'binary',
        boolean => 'boolean',
        dateTime => 'yang:date-and-time',
        hexBinary => 'yang:hex-string',
        int => 'int32',
        long => 'int64',
        unsignedInt => 'uint32',
        unsignedLong => 'uint64',
        Alias => 'types:Alias',
        Dbm1000 => 'types:Dbm1000',
        DiagnosticsState => 'types:DiagnosticsState',
        IEEE_EUI64 => 'types:IEEE_EUI64',
        IPAddress => 'types:IPAddress',
        IPv4Address => 'types:IPv4Address',
        IPv6Address => 'types:IPv6Address',
        IPPrefix => 'types:IPPrefix',
        IPv4Prefix => 'types:IPv4Prefix',
        IPv6Prefix => 'types:IPv6Prefix',
        MACAddress => 'types:MACAddress',
        StatsCounter32 => 'types:StatsCounter32',
        StatsCounter64 => 'types:StatsCounter64',
        UUID => 'yang:uuid',
        ZigBeeNetworkAddress => 'types:ZigBeeNetworkAddress'
    };
    $type = $dm_to_yang_type_map->{$type} if
        defined $dm_to_yang_type_map->{$type};

    my $ranges = get_ranges($node, $state);
    my $lengths = get_lengths($node, $state);
    my $patterns = get_patterns($node, $state);
    my $enums = get_enums($node, $state);

    # YANG enumerations are "enumeration" rather than "string"
    $type = 'enumeration' if $enums;

    my $has_content = $ranges || $lengths || $patterns || $enums;
    my $opt_brace = $has_content ? qq{ \{} : qq{;};
    
    # XXX temporarily indicate if it's a command parameter; these and other
    #     parameters that should be command parameters can be converted to
    #     RPCs?
    my $command = $syntax->{command} ? qq{ /* command */} : qq{};

    output $i+1, qq{type $type$opt_brace$command};

    if ($has_content) {
        output $i+2, $ranges if $ranges;
        output $i+2, $lengths if $lengths;
        output $i+2, $patterns if $patterns;
        output $i+2, $enums if $enums;
        output $i+1, qq{\}};
    }

    my $config = get_config($node, $state);
    output $i+1, $config if $config;

    my $default = get_default($node, $state);
    output $i+1, $default if $default;

    my $description = get_description($node, $i+2, $state);
    output $i+1, $description if $description;

    output $i, qq{\}};
}

sub output_container_close {
    my ($i, $node, $state) = @_;

    output $i, qq{\}};
}

sub output_list_close {
    my ($i, $node, $state) = @_;

    output $i, qq{\}};
}

# output module augments
sub output_augments {
    my ($i, $module) = @_;
    
}

# output module RPCs
sub output_rpcs {
    my ($i, $module) = @_;
    
}

# output module notifications
sub output_notifications {
    my ($i, $module) = @_;
    
}

sub get_config {
    my ($node, $state) = @_;
    
    # determine parent object's config; 1 if no parent object
    my $pconfig = ($node->{pnode} && $node->{pnode}->{type} eq 'object') ?
        $node->{pnode}->{dm2yang_config} : 1;

    # config was determined during node traversal
    my $config = $node->{dm2yang_config};

    # per RFC 6087 section 4.3, generate the config substatement only on
    # transition
    my $cfgstr = ($config != $pconfig) ?
        (qq{config } . ($config ? 'true' : 'false') . qq{;}) : qq{};

    return $cfgstr;
}

sub get_status {
    my ($node, $state) = @_;

    my $status = $node->{status};

    # XXX not covering status=deleted
    $status = 'obsolete' if $status eq 'obsoleted';

    my $stsstr = ($status ne 'current') ? qq{status $status;} : qq{};

    return $stsstr;
}
    
sub get_ranges {
    my ($node, $state) = @_;

    my $path = $node->{path};
    my $syntax = $node->{syntax};

    my $ranges = $syntax->{ranges};

    my $rngstr = qq{};
    if ($ranges && @$ranges) {
        $rngstr .= qq{range \"};
        my $first = 1;
        foreach my $range (@$ranges) {
            my $min = $range->{minInclusive};
            my $max = $range->{maxInclusive};
            my $step = $range->{step};

            $min = 'min' unless defined $min && $min ne ''; 
            $max = 'max' unless defined $max && $max ne ''; 

            # XXX YANG doesn't support step
            main::emsg "$path: step $step not supported (will need to " .
                " scale parameter); ignored"
                if defined $step && $step ne '' && $step != 1;

            # XXX not covering all cases, e.g. min > max, disjoint, ascending
            $rngstr .= qq{ | } unless $first;
            if ($min ne 'min' && $max ne 'max' && $max == $min) {
                $rngstr .= qq{$min};
            } else {
                $rngstr .= qq{$min..$max};
            }

            $first = 0;
        }
        $rngstr .= qq{\";};
    }

    return $rngstr;
}
    
sub get_lengths {
    my ($node, $state) = @_;

    my ($node, $state) = @_;

    my $path = $node->{path};
    my $syntax = $node->{syntax};

    my $sizes = $syntax->{sizes};

    my $lenstr = qq{};
    if ($sizes && @$sizes) {
        $lenstr .= qq{length \"};
        my $first = 1;
        foreach my $size (@$sizes) {
            my $min = $size->{minLength};
            my $max = $size->{maxLength};

            $min = 'min' unless defined $min && $min ne ''; 
            $max = 'max' unless defined $max && $max ne '';

            $min = '0' if $min eq 'min';

            # XXX not covering all cases, e.g. min > max, disjoint, ascending
            $lenstr .= qq{ | } unless $first;
            if ($min ne 'min' && $max ne 'max' && $max == $min) {
                $lenstr .= qq{$min};
            } else {
                $lenstr .= qq{$min..$max};
            }

            $first = 0;
        }
        $lenstr .= qq{\";};
    }

    return $lenstr;
}
    
sub get_patterns {
    my ($node, $state) = @_;

    return get_values($node, $state, 'pattern');
}

sub get_enums {
    my ($node, $state) = @_;

    return get_values($node, $state, 'enumeration');
}

# helper for get_patterns and get_enums
# XXX not covering status, description etc
sub get_values {
    my ($node, $state, $filter) = @_;

    my $values = $node->{values};

    # map from DM facet name (pattern or enumeration) to the YANG statement
    # name (pattern or enum)
    my $facet_map = {pattern => 'pattern', enumeration => 'enum'};

    my $valstr = qq{};
    if ($values && %$values) {
        foreach my $value (sort {$values->{$a}->{i} <=>
                                     $values->{$b}->{i}} keys %$values) {
            my $cvalue = $values->{$value};

            # filter has to be the DM facet name: pattern or enumeration
            my $facet = $cvalue->{facet};
            next unless $facet eq $filter;

            my $status = $cvalue->{status};
            next if $status =~ /^(deleted)$/i;

            my $stmt = $facet_map->{$facet};

            # XXX problem if value contains a double quote or other illegal
            #     character
            # XXX no support for enum/value; needs to come from DM "code" but
            #     that's not currently parsed
            # XXX could use helper to decide whether to quote
            $valstr.= qq{\n$stmt \"$value\";}
        }
    }

    return $valstr;
}

sub get_default {
    my ($node, $state) = @_;

    my $default = $node->{default};
    my $deftype = $node->{deftype};
    my $defstat = $node->{defstat};

    my $defstr = qq{};

    # XXX ignoring object/factory distinction, different DM/YANG semantics, and
    #     default status
    if (defined $default) {
        $defstr .= qq{default "$default";}
    }

    return $defstr;
}

# XXX should allow this also to be used for pattern/enum descriptions, and
#     should add the code to invoke it in such cases (and other cases where
#     descriptions are supported)
sub get_description {
    my ($node, $i, $state) = @_;

    my $description = $node->{description};
    my $descact = $node->{descact};
    my $changed = $node->{changed};
    my $history = $node->{history};

    ($description, $descact) = main::get_description(
        $description, $descact, $changed->{description}, $history, 1);

    # XXX could/should also find non-ASCII open/close quote characters?
    $description =~ s/\"/\\\"/g;

    # XXX this is a short-term hack; it doesn't do anything with tabs; long
    #     lines can still occur; should fully implement RFC 6020 section 6.1.3
    #     (Quoting)
    my $format = Text::Format->new(
        {
            columns => 70 - 3 - 2*$i,
            extraSpace => 1,
            firstIndent => 0,
            bodyIndent => 3
        });

    my @paragraphs = split /\n/, $description;

    my $first = 1;
    $description = qq{};
    foreach my $paragraph (@paragraphs) {
        $format->firstIndent($first ? 0 : 3);
        $paragraph = $format->format($paragraph);
        $description .= qq{\n} if $description;
        $description .= $paragraph;
        $first = 0;
    }

    $description =~ s/\n$//;
    
    my $dscstr = qq{};

    # XXX ignoring formatting
    if ($description) {
        $dscstr .= qq{description\n  "$description";}
    }

    return $dscstr;
}

# determine parent object's config; 1 if no parent object
# output multi-line string to stdout, handling indentation
# or if evaluated in scalar context, return a string instead (with newlines)
# or if evaluated in list context, return a list of lines (no newlines)
# XXX this is taken from map.pm
sub output
{
    my ($indent, $lines) = @_;

    # ignore initial and final newlines (cosmetic)
    $lines =~ s/^\n?//;
    $lines =~ s/\n?$//;

    # collect output lines in a list (no newlines)
    my @lines = ();
    foreach my $line (split /\n/, $lines) {
        push @lines, '  ' x $indent . $line;
    }

    # special case: treat no lines as single empty line
    push @lines, '' unless @lines;

    # if the caller wants no value, output to stdout with newlines
    if (!defined wantarray) {
        foreach my $line (@lines) {
            print $line, "\n";
        }
    }

    # if the caller wants a scalar, join with newlines, including trailing one
    elsif (!wantarray) {
        my $text = join "\n", @lines;
        $text .= "\n" if $text;
        return $text;
    }

    # if the caller wants a list, return the list
    else {
        return @lines;
    }
}

# end of plugin
1;
