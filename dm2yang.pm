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

    # use objects and parameters; ignore #entries parameters
    my $use_node = $type eq 'object' || $syntax;
    my $ignore_node = $syntax && $node->{table};
    push @{$module->{nodes}}, $node if $use_node && !$ignore_node;
}

# this is called after all nodes have been processed
sub dm2yang_end {
    # output modules
    output_modules($modules);
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
    my $state = {config => 1};

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

    my $config = get_config($node, $state);
    
    output $i, qq{

container $name \{$config
};
}

sub output_list_open {
    my ($i, $node, $state) = @_;

    my $name = $node->{name};
    my $access = $node->{access};
    my $uniqueKeys = $node->{uniqueKeys};
    
    $name =~ s/\.\{i\}\.$//;

    my $config = get_config($node, $state);
    
    # prefer the first functional unique key as "key" and any others as
    # "unique"
    # XXX this logic is adapted from main:xml2_node
    # XXX if no unique keys for writable table (config true), should invent an
    #     "instanceNumber" one?
    # XXX should use a get_key routine; combine with get_unique?
    my $key = undef;
    if ($uniqueKeys) {
        ($key) = grep {$_->{functional}} @$uniqueKeys;
        ($key) = grep {!$_->{functional}} @$uniqueKeys unless $key;       
        if ($key) {
            my $temp = join ' ', @{$key->{keyparams}};
            $key = qq{key "$temp";};
        }
    }

    # if key is non-empty, prefix with "\n  " to ease caller logic
    $key = qq{\n  $key} if $key;

    output $i, qq{

list $name \{$key$config
};
}

sub output_leaf {
    my ($i, $node, $state) = @_;

    my $name = $node->{name};
    my $access = $node->{access};
    my $type = $node->{type};
    my $syntax = $node->{syntax};

    my $config = get_config($node, $state);
    
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
        dateTime => 'yang:date-and-time',
        hexBinary => 'yang:hex-string',
        int => 'int32',
        unsignedInt => 'uint32',
        Alias => 'types:Alias',
        IPAddress => 'types:IPAddress',
        UUID => 'yang:uuid'
    };
    $type = $dm_to_yang_type_map->{$type} if
        defined $dm_to_yang_type_map->{$type};
    
    output $i, qq{
leaf $name {$config
  type $type;
}
};
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

# return empty string or "config false/true;" depending on whether config is
# different from parent config
sub get_config {
    my ($node, $state) = @_;
    
    my $path = $node->{path};
    my $access = $node->{access};
    my $fixedObject = $node->{fixedObject};

    # determine parent object's config; 1 if no parent object
    my $pconfig = ($node->{pnode} && $node->{pnode}->{type} eq 'object') ?
        $node->{pnode}->{access} eq 'readWrite' : 1;

    # config true/false corresponds to access readWrite/readOnly, except that
    # readOnly fixedObject has config true
    my $config = $access eq 'readWrite';
    $config = 1 if $fixedObject;

    # output error message on false -> true transitions
    # XXX suppressed for now because there are so many of them; need to decide
    #     what to do here
    main::emsg "$path: parent/child access transition from readOnly to " .
        "readWrite; forbidden by YANG" if !$pconfig && $config;

    # per RFC 6087 section 4.3, generate the config substatement only on
    # transition
    my $cfgstr = ($config != $pconfig) ?
        (qq{config } . ($config ? 'true' : 'false') . qq{;}) : qq{};

    # if returning non-empty string, prefix with "\n  " to ease caller logic
    $cfgstr = qq{\n  $cfgstr} if $cfgstr;
    
    return $cfgstr;
}

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
