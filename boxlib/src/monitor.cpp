#include <bubblebox/utilities.h>
#include <string.h>
/*
*
*
*/
using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{

    Monitor::Monitor(const char *_type): max_progress(0), progress(0)
    {
        if(strcmp(_type,"action") == 0)
        {

            type = "action";

            bar.set_option(indicators::option::Start{"["});
            bar.set_option(indicators::option::Fill{"■"});
            bar.set_option(indicators::option::Lead{"■"});
            bar.set_option(indicators::option::Remainder{"-"});
            bar.set_option(indicators::option::End{"]"});
            bar.set_option(indicators::option::ShowPercentage{true});
            bar.set_option(indicators::option::ForegroundColor{indicators::Color::cyan});
            bar.set_option(indicators::option::BarWidth{50});
            bar.set_option(indicators::option::FontStyles{std::vector<indicators::FontStyle>
                                                         {indicators::FontStyle::bold}});

        }
    }


    void Monitor::setlimit(int iterlimit)
    {
        max_progress = iterlimit;
        bar.set_option(indicators::option::MaxProgress{max_progress});
    }
    

    void Monitor::update(std::string message,int _progress)
    {
        if(strcmp(type,"action") == 0)
        {
            ++progress;
            bar.set_option(indicators::option::PrefixText{message});
            bar.tick();
        }
    }

}
