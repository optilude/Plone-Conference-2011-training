# VCL file optimized for plone.app.caching.  See vcl(7) for details

# This is an example of a split view caching setup with another proxy
# like Apache in front of Varnish to rewrite urls into the VHM style.

# Also assumes a single backend behind Varnish (which could be a single
# zope instance or a load balancer serving multiple zeo clients).
# To change this to support multiple backends, see the vcl man pages
# for instructions.


# Configure balancer server as back end
backend balancer {
    .host = "${hosts:varnish-backend}";
    .port = "${ports:varnish-backend}";
}

# Only allow PURGE from localhost
acl purge {
    "${hosts:allow-purge}";
}

sub vcl_recv {
    set req.grace = 10m;
    set req.backend = balancer;
    
    if (req.request == "PURGE") {
        if (!client.ip ~ purge) {
                error 405 "Not allowed.";
        }
        purge_url(req.url);
        error 200 "Purged";
    }
    if (req.request != "GET" && req.request != "HEAD") {
        # We only deal with GET and HEAD by default
        return(pass);
    }
    call normalize_accept_encoding;
    call annotate_request;
    return(lookup);
}

sub vcl_fetch {
    if (!beresp.cacheable) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - not cacheable)";
        return(pass);
    }
    if (beresp.http.Set-Cookie) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets cookie)";
        return(pass);
    }
    if (!beresp.http.Cache-Control ~ "s-maxage=[1-9]" && beresp.http.Cache-Control ~ "(private|no-cache|no-store)") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets private/no-cache/no-store token)";
        return(pass);
    }
    if (!req.http.X-Anonymous && !beresp.http.Cache-Control ~ "public") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - authorized and no public cache control)";
        return(pass);
    }
    if (req.http.X-Anonymous && !beresp.http.Cache-Control) {
        set beresp.ttl = 10s;
        set beresp.http.X-Varnish-Action = "FETCH (override - backend not setting cache control)";
    } else {
        set beresp.http.X-Varnish-Action = "FETCH (deliver)";
    }
    call rewrite_s_maxage;
    return(deliver);
}

sub vcl_deliver {
    call rewrite_age;
}


##########################
#  Helper Subroutines
##########################

# Optimize the Accept-Encoding variant caching
sub normalize_accept_encoding {
    if (req.http.Accept-Encoding) {
        if (req.url ~ "\.(jpe?g|png|gif|swf|pdf|gz|tgz|bz2|tbz|zip)$" || req.url ~ "/image_[^/]*$") {
            remove req.http.Accept-Encoding;
        } elsif (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } else {
            remove req.http.Accept-Encoding;
        }
    }
}

# Keep auth/anon variants apart if "Vary: X-Anonymous" is in the response
sub annotate_request {
    if (!(req.http.Authorization || req.http.cookie ~ "(^|.*; )__ac=")) {
        set req.http.X-Anonymous = "True";
    }
}

# The varnish response should always declare itself to be fresh
sub rewrite_age {
    if (resp.http.Age) {
        set resp.http.X-Varnish-Age = resp.http.Age;
        set resp.http.Age = "0";
    }
}

# Rewrite s-maxage to exclude from intermediary proxies
# (to cache *everywhere*, just use 'max-age' token in the response to avoid this override)
sub rewrite_s_maxage {
    if (beresp.http.Cache-Control ~ "s-maxage") {
        set beresp.http.Cache-Control = regsub(beresp.http.Cache-Control, "s-maxage=[0-9]+", "s-maxage=0");
    }
}
