#include <bubblebox/utilities.h>
#include <string.h>
/*
*
*
*/
using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{

    Monitor::Monitor(const char *bartype): max_progress(0), progress(0)
    {
        if(strcmp(bartype,"action") == 0)
        {
            progressBar.set_option(indicators::option::Start{"["});
            progressBar.set_option(indicators::option::Fill{"="});
            progressBar.set_option(indicators::option::Lead{">"});
            progressBar.set_option(indicators::option::Remainder{" "});
            progressBar.set_option(indicators::option::End{" ]"});
            progressBar.set_option(indicators::option::ShowPercentage{true});
            progressBar.set_option(indicators::option::ForegroundColor{indicators::Color::green});
            progressBar.set_option(indicators::option::BarWidth{50});
            progressBar.set_option(indicators::option::FontStyles{std::vector<indicators::FontStyle>
                                                                 {indicators::FontStyle::bold}});
        }
    }


    void Monitor::setIterLimit(int iterlimit)
    {
        max_progress = iterlimit;
        progressBar.set_option(indicators::option::MaxProgress{max_progress});
    }
    


    void Monitor::updateBar()
    {
        ++progress;
        progressBar.set_option(indicators::option::PostfixText{std::to_string(progress) + "/" + 
                                                               std::to_string(max_progress)});
        progressBar.tick();
    }

}
